import logging
import os
from google.cloud import bigquery
from django.core.cache import cache
from datetime import timedelta

logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./pro-hour-450500-v1-1e44b3cf5db5.json"
BIGQUERY_TABLE_ID = "pro-hour-450500-v1.apollo.listkit_contacts"

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
        id, full_name, business_email, additional_personal_emails, company_name, 
        job_title, industry_name, company_country_name, company_size, 
        employees_range, mobile_phone, personal_phone, company_phone, 
        company_domain, linkedin_url, company_linkedin_url, company_logo, description,
        created_at, updated_at 
    FROM `{BIGQUERY_TABLE_ID}`
    WHERE 1=1
    """

    query_params = []
    
    if filters:
        for field, values in filters.items():
            if isinstance(values, list):
                # Handle multiple values for the same field with OR
                conditions = [f"{field} = @{field}_{i}" for i in range(len(values))]
                base_query += f" AND ({' OR '.join(conditions)})"
                for i, value in enumerate(values):
                    query_params.append(bigquery.ScalarQueryParameter(f"{field}_{i}", "STRING", value))
            else:
                # Handle single value
                base_query += f" AND {field} = @{field}"
                query_params.append(bigquery.ScalarQueryParameter(field, "STRING", values))

    # Add ORDER BY clause
    if order_by:
        base_query += f" ORDER BY {order_by}"
    else:
        base_query += " ORDER BY created_at DESC"  # Default ordering

    # Add LIMIT and OFFSET
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
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
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

def get_unique_values(field_name, limit=None):
    """Get unique values for a field from BigQuery with caching"""
    cache_key = f'bigquery_unique_{field_name}'
    cached_values = cache.get(cache_key)
    
    if cached_values is not None:
        print(f"DEBUG: Using cached values for {field_name}")
        return cached_values[:limit] if limit else cached_values
        
    print(f"DEBUG: Fetching unique values for {field_name} from BigQuery")
    client = bigquery.Client()
    
    query = f"""
    SELECT DISTINCT {field_name}
    FROM `{BIGQUERY_TABLE_ID}`
    WHERE {field_name} IS NOT NULL
    ORDER BY {field_name}
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        values = [row[field_name] for row in results]
        
        # Cache for 24 hours
        cache.set(cache_key, values, timeout=86400)  # 24 hours in seconds
        
        return values[:limit] if limit else values
    except Exception as e:
        logger.error(f"Error fetching unique values for {field_name}: {str(e)}", exc_info=True)
        return []
