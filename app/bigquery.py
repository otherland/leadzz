import logging
import os
from google.cloud import bigquery
from django.core.cache import cache
from datetime import timedelta
import json

logger = logging.getLogger(__name__)

credentials_file = "./pro-hour-450500-v1-1e44b3cf5db5.json"

# Check if credentials file exists first
if os.path.exists(credentials_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file
# Fall back to environment variables if file doesn't exist
elif not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    credentials_dict = {
        "type": "service_account",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
    }
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = json.dumps(credentials_dict)

BIGQUERY_TABLE_ID = "pro-hour-450500-v1.apollo.listkit_contacts_optimized"

def fetch_contacts(filters=None, limit=50, offset=0, order_by=None):
    # Create a cache key based on the query parameters
    params = {
        "filters": str(filters),
        "limit": limit,
        "offset": offset,
        "order_by": order_by
    }
    cache_key = f'contacts_query_{hash(frozenset(params.items()))}'
    
    # Try to get cached results
    cached_results = cache.get(cache_key)
    if cached_results is not None:
        print("DEBUG: Using cached query results")
        return cached_results

    client = bigquery.Client()
    
    base_query = f"""
    SELECT 
        full_name, company_name, job_title, industry_name,
        company_country_name, employees_range, company_domain,
        linkedin_url, company_linkedin_url, company_logo, description
    FROM `{BIGQUERY_TABLE_ID}`
    WHERE 1=1
    """

    query_params = []
    
    if filters:
        # Optimize the filter conditions
        filter_conditions = []
        for field, values in filters.items():
            if isinstance(values, list):
                # Use IN clause for multiple values instead of multiple OR conditions
                placeholders = [f"@{field}_{i}" for i in range(len(values))]
                filter_conditions.append(f"{field} IN ({', '.join(placeholders)})")
                for i, value in enumerate(values):
                    query_params.append(bigquery.ScalarQueryParameter(f"{field}_{i}", "STRING", value))
            else:
                filter_conditions.append(f"{field} = @{field}")
                query_params.append(bigquery.ScalarQueryParameter(field, "STRING", values))
        
        if filter_conditions:
            base_query += f" AND {' AND '.join(filter_conditions)}"

    # Simplified ordering
    base_query += f" LIMIT @limit OFFSET @offset"
    query_params.extend([
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
        bigquery.ScalarQueryParameter("offset", "INT64", offset)
    ])

    print("\nDEBUG: BigQuery Details:")
    print(f"  Query: {base_query}")
    print(f"  Parameters: {query_params}")
    print(f"  Limit: {limit}, Offset: {offset}")

    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=query_params,
            use_query_cache=True  # Explicitly enable query cache
        )
        query_job = client.query(base_query, job_config=job_config)
        results = query_job.result()
        result_list = [dict(row.items()) for row in results]
        print(f"  Results returned: {len(result_list)}")
        
        # Cache the results for 5 minutes
        cache.set(cache_key, result_list, timeout=300)  # 300 seconds = 5 minutes
        
        return result_list
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        logger.error(f"BigQuery error: {str(e)}", exc_info=True)
        raise

def get_unique_values(field_name, limit=1000):
    """Get unique values for a field with caching"""
    cache_key = f'unique_values_{field_name}'
    cached_values = cache.get(cache_key)
    
    if cached_values is not None:
        return cached_values

    client = bigquery.Client()
    
    query = f"""
    SELECT DISTINCT {field_name}
    FROM `{BIGQUERY_TABLE_ID}`
    WHERE {field_name} IS NOT NULL
    ORDER BY {field_name}
    LIMIT @limit
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ],
        use_query_cache=True
    )

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        # Extract values and filter out None/empty
        values = [row[field_name] for row in results if row[field_name]]
        
        # Cache for 1 hour (3600 seconds)
        cache.set(cache_key, values, timeout=3600)
        
        return values
    except Exception as e:
        logger.error(f"BigQuery error in get_unique_values: {str(e)}", exc_info=True)
        return []

def get_filtered_count(filters=None):
    """Get total count of contacts matching the filters"""
    if not filters:
        cache_key = 'contacts_count_total'
    else:
        # Create a stable cache key from the filters
        filter_items = []
        for k, v in sorted(filters.items()):
            if isinstance(v, list):
                filter_items.extend((k, item) for item in sorted(v))
            else:
                filter_items.append((k, v))
        cache_key = f'contacts_count_{"_".join(str(x) for x in filter_items)}'
    
    # Try to get cached count
    cached_count = cache.get(cache_key)
    if cached_count is not None:
        return cached_count

    client = bigquery.Client()
    
    count_query = f"""
    SELECT COUNT(1) as total
    FROM `{BIGQUERY_TABLE_ID}`
    WHERE 1=1
    """

    query_params = []
    
    if filters:
        filter_conditions = []
        for field, values in filters.items():
            if isinstance(values, list) and values:
                values = [v for v in values if v]  # Remove empty values
                if values:  # Only add condition if we have values
                    placeholders = [f"@{field}_{i}" for i in range(len(values))]
                    filter_conditions.append(f"{field} IN ({', '.join(placeholders)})")
                    for i, value in enumerate(values):
                        query_params.append(bigquery.ScalarQueryParameter(f"{field}_{i}", "STRING", value))
            elif values:  # Single non-empty value
                filter_conditions.append(f"{field} = @{field}")
                query_params.append(bigquery.ScalarQueryParameter(field, "STRING", values))
        
        if filter_conditions:
            count_query += f" AND {' AND '.join(filter_conditions)}"

    print(f"\nDEBUG Count Query: {count_query}")
    print(f"DEBUG Count Params: {query_params}")

    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=query_params,
            use_query_cache=True
        )
        query_job = client.query(count_query, job_config=job_config)
        result = next(query_job.result())
        total_count = result.total
        
        print(f"DEBUG Count Result: {total_count} for filters: {filters}")
        
        # Cache the count for 5 minutes
        cache.set(cache_key, total_count, timeout=300)
        
        return total_count
    except Exception as e:
        logger.error(f"BigQuery count error: {str(e)}", exc_info=True)
        return 0
