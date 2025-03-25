#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Metadata Module
------------------------
A module for handling Yoast SEO and other metadata in WordPress posts.
This module provides functions to add metadata to WordPress posts,
including SEO metadata, OpenGraph metadata, and Twitter card metadata.
"""

import json
import requests
from datetime import datetime
import re

def add_meta_to_post_data(post_data, title, content, meta_content):
    """Add meta description and keyphrases to post data for WordPress.
    
    Args:
        post_data (dict): The post data dictionary to which metadata will be added
        title (str): The post title
        content (str): The post content
        meta_content (dict): Dictionary containing meta_description and keyphrases
        
    Returns:
        dict: The updated post_data dictionary with metadata added
    """
    # Initialize meta object if not already present
    if 'meta' not in post_data:
        post_data['meta'] = {}
    
    # Handle meta description
    meta_description = meta_content.get('meta_description', '')
    if meta_description:
        # Add Yoast SEO metadata for various configurations
        _add_yoast_meta_description(post_data, title, meta_description)
        
        # Add as standard WordPress excerpt as backup (trimmed to 160 chars)
        if len(meta_description) > 160:
            post_data['excerpt'] = {'rendered': meta_description[:157] + '...'}
        else:
            post_data['excerpt'] = {'rendered': meta_description}
    
    # Handle keyphrases for Yoast SEO
    keyphrases = meta_content.get('keyphrases', [])
    if keyphrases:
        _add_yoast_keyphrases(post_data, title, keyphrases)
    
    # Add additional Yoast schema and article metadata
    _add_yoast_schema_data(post_data, content)
    
    return post_data

def _add_yoast_meta_description(post_data, title, meta_description):
    """Add Yoast SEO meta description fields to post data.
    
    Args:
        post_data (dict): The post data dictionary
        title (str): The post title
        meta_description (str): The meta description to add
    """
    # Ensure we don't exceed Yoast's limit
    if len(meta_description) > 160:
        meta_description = meta_description[:157] + '...'
    
    # Format the title in the way Yoast stores it (with site name using %%sep%% delimiter)
    yoast_title = title  # Simple version
    yoast_title_with_sep = f"{title} %%sep%% %%sitename%%"  # Yoast separator version
    
    # The most critical Yoast fields - these are the ones that definitely need to be set
    # These are the actual fields WordPress stores in the database 
    post_data['meta']['_yoast_wpseo_metadesc'] = meta_description
    post_data['meta']['_yoast_wpseo_title'] = yoast_title_with_sep
    
    # OpenGraph and Twitter fields - these are important for social sharing
    post_data['meta']['_yoast_wpseo_opengraph-title'] = title
    post_data['meta']['_yoast_wpseo_opengraph-description'] = meta_description
    post_data['meta']['_yoast_wpseo_twitter-title'] = title
    post_data['meta']['_yoast_wpseo_twitter-description'] = meta_description
    
    # Newer versions of Yoast also use canonical fields
    post_data['meta']['_yoast_wpseo_canonical'] = ""  # Will be filled by WordPress
    
    # Include non-underscore versions for compatibility
    post_data['meta']['yoast_wpseo_metadesc'] = meta_description
    post_data['meta']['yoast_wpseo_title'] = yoast_title
    
    # Legacy fields
    post_data['meta']['_yoast_seo_title'] = title
    post_data['meta']['_yoast_seo_metadesc'] = meta_description
    
    # Direct custom fields
    post_data['meta']['metadesc'] = meta_description
    post_data['meta']['title'] = title
    
    # Some WordPress installations use these non-prefixed versions
    post_data['yoast_meta_description'] = meta_description
    post_data['yoast_title'] = title
    post_data['yoast_wpseo_metadesc'] = meta_description
    
    # For All in One SEO (alternative SEO plugin)
    post_data['meta']['_aioseop_description'] = meta_description
    post_data['meta']['_aioseop_title'] = title
    
    # Additional fields for Yoast indexing settings
    post_data['meta']['_yoast_wpseo_meta-robots-noindex'] = '0'  # 0 = indexed, 1 = noindex
    post_data['meta']['_yoast_wpseo_meta-robots-nofollow'] = '0'  # 0 = follow, 1 = nofollow
    post_data['meta']['_yoast_wpseo_meta-robots-adv'] = 'none'  # Additional robot instructions

def _add_yoast_keyphrases(post_data, title, keyphrases):
    """Add Yoast SEO keyphrase fields to post data.
    
    Args:
        post_data (dict): The post data dictionary
        title (str): The post title
        keyphrases (list): List of keyphrases to add
    """
    # Ensure keyphrases is a list
    if not isinstance(keyphrases, list):
        keyphrases = [keyphrases] if keyphrases else []
        
    # Primary keyphrase (first one)
    primary_keyphrase = keyphrases[0] if keyphrases else ''
    post_data['meta']['_yoast_wpseo_focuskw'] = primary_keyphrase
    
    # Include the keyphrase in the meta title for better SEO
    if primary_keyphrase and 'meta' in post_data and '_yoast_wpseo_title' in post_data['meta']:
        # Only add if not already included in the title
        existing_title = post_data['meta']['_yoast_wpseo_title']
        if primary_keyphrase.lower() not in existing_title.lower() and '%%sep%%' in existing_title:
            # Replace the default title with one that includes the keyphrase
            parts = existing_title.split('%%sep%%')
            if len(parts) >= 2:
                new_title = f"{parts[0].strip()} - {primary_keyphrase} %%sep%% {parts[1].strip()}"
                post_data['meta']['_yoast_wpseo_title'] = new_title
    
    # Secondary keyphrases (rest of the list)
    if len(keyphrases) > 1:
        # For keyword synonyms - Yoast uses a comma-separated string
        secondary_keyphrases = ', '.join(keyphrases[1:])
        post_data['meta']['_yoast_wpseo_keywordsynonyms'] = secondary_keyphrases
        
        # For related keyphrases (in Yoast Premium) - uses a specific JSON format
        related_keyphrases = []
        for i, keyphrase in enumerate(keyphrases[1:5]):  # Limit to 4 related keyphrases
            related_keyphrases.append({
                "value": keyphrase, 
                "key": f"additional_keyphrase_{i+1}"
            })
        
        if related_keyphrases:
            # Yoast expects this exact format for additional keyphrases
            post_data['meta']['_yoast_wpseo_focuskeywords'] = json.dumps(related_keyphrases)
    
    # Add content score field that Yoast calculates 
    # Using a mid-range value so it shows up in Yoast dashboard for editing
    post_data['meta']['_yoast_wpseo_content_score'] = '60'
    
    # Additional keyphrase fields Yoast might use for specific versions
    if primary_keyphrase:
        # Some older or specific versions of Yoast use these fields
        post_data['meta']['_yoast_wpseo_focuskeywords_text_input'] = primary_keyphrase
        post_data['meta']['focus_keyword'] = primary_keyphrase

def _add_yoast_schema_data(post_data, content):
    """Add Yoast SEO schema and article data to post data.
    
    Args:
        post_data (dict): The post data dictionary
        content (str): The post content
    """
    # Set SEO score to 'needs improvement' to make it show up in Yoast dashboard
    post_data['meta']['_yoast_wpseo_content_score'] = '60'
    
    # Additional fields from Yoast schema
    post_data['meta']['_yoast_wpseo_schema_article_type'] = 'BlogPosting'
    post_data['meta']['_yoast_wpseo_estimated-reading-time-minutes'] = str(max(1, round(len(content.split()) / 250)))
    
    # Try to get the current date in the format Yoast expects
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    post_data['meta']['_yoast_wpseo_schema-page-type'] = 'article'
    post_data['meta']['_yoast_wpseo_schema-article-type'] = 'BlogPosting'

def update_post_meta(wp_url, post_id, meta_content, headers, debug=False):
    """Update Yoast SEO metadata for an existing post.
    
    Args:
        wp_url (str): WordPress site URL
        post_id (int): ID of the post to update
        meta_content (dict): Dictionary containing meta_description and keyphrases
        headers (dict): Headers to use for authentication
        debug (bool): Whether to print debug information
        
    Returns:
        bool: True if at least one update method was successful, False otherwise
    """
    if not post_id or not meta_content:
        return False
    
    # Prepare post data with just the meta fields
    post_data = {'meta': {}}
    title = meta_content.get('title', '')
    content = meta_content.get('content', '')
    
    # Add meta fields to post_data
    post_data = add_meta_to_post_data(post_data, title, content, meta_content)
    
    # Check if we have any meta fields to update
    if not post_data.get('meta'):
        return False
    
    # Debug information
    if debug:
        print("\nYoast SEO Metadata being sent for update:")
        for key, value in post_data['meta'].items():
            if key.startswith('_yoast'):
                print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
    
    # Attempt different methods to update meta fields
    success = False
    
    # Attempt 1: Try PUT request to update the post with meta fields
    try:
        update_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        update_data = {'meta': post_data['meta']}
        print(f"Attempt 1: Updating post with meta fields via PUT to {update_url}")
        update_response = requests.put(update_url, headers=headers, json=update_data)
        
        if update_response.status_code in [200, 201]:
            print("Successfully updated meta data via PUT request.")
            success = True
        else:
            print(f"PUT update failed: HTTP {update_response.status_code}")
            if debug:
                print(f"Response: {update_response.text[:200]}...")
    except Exception as e:
        print(f"Error in Attempt 1: {e}")
    
    # Attempt 2: Try updating each meta field individually via REST API
    if not success:
        try:
            print("Attempt 2: Updating each meta field individually")
            individual_success = False
            
            # Get the current post to verify we can access it
            get_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
            get_response = requests.get(get_url, headers=headers)
            
            if get_response.status_code == 200:
                # First method: Update post with only one meta field at a time
                for key, value in post_data['meta'].items():
                    # Skip non-Yoast fields to focus on what matters
                    if not (key.startswith('_yoast') or key.startswith('yoast')):
                        continue
                        
                    # Create a payload with just this one meta field
                    single_meta = {'meta': {key: value}}
                    single_update_response = requests.put(
                        get_url, 
                        headers=headers, 
                        json=single_meta
                    )
                    
                    if single_update_response.status_code in [200, 201]:
                        print(f"Successfully updated {key}")
                        individual_success = True
                    else:
                        print(f"Failed to update {key}: HTTP {single_update_response.status_code}")
                
                if individual_success:
                    print("Successfully updated at least one meta field individually")
                    success = True
            else:
                print(f"Cannot retrieve post: HTTP {get_response.status_code}")
        except Exception as e:
            print(f"Error in Attempt 2: {e}")
            
    # Attempt 3: Try standard WP REST meta endpoints directly 
    if not success:
        try:
            print("Attempt 3: Using WP REST API meta endpoints directly")
            meta_endpoint_success = False
            
            # Create endpoints for both meta and yoast
            wp_meta_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}/meta"
            
            # Try to use the WordPress meta endpoint
            for key, value in post_data['meta'].items():
                # Only try important fields to avoid too many requests
                if not (key.startswith('_yoast_wpseo_metadesc') or key.startswith('_yoast_wpseo_title')):
                    continue
                    
                meta_payload = {key: value}
                meta_response = requests.post(wp_meta_url, headers=headers, json=meta_payload)
                
                if meta_response.status_code in [200, 201]:
                    print(f"Successfully updated {key} via meta endpoint")
                    meta_endpoint_success = True
                else:
                    print(f"Failed to update {key} via meta endpoint: HTTP {meta_response.status_code}")
            
            if meta_endpoint_success:
                print("Successfully updated metadata using REST API meta endpoints")
                success = True
        except Exception as e:
            print(f"Error in Attempt 3: {e}")
    
    # Attempt 4: Try using WordPress core update_post_meta approach 
    if not success:
        try:
            print("Attempt 4: Using custom endpoint for direct WordPress function access")
            
            # Check if site has WP REST API Meta Fields plugin or similar functionality
            # This would normally require a plugin that exposes update_post_meta as an endpoint
            custom_meta_url = f"{wp_url.rstrip('/')}/wp-json/wp-meta/v1/update"
            
            # Check if the endpoint exists
            options_response = requests.options(custom_meta_url)
            if options_response.status_code not in [200, 204, 404]:
                print(f"Custom meta endpoint might exist: {options_response.status_code}")
                
                # Try to update the critical fields
                meta_desc = post_data['meta'].get('_yoast_wpseo_metadesc', '')
                meta_title = post_data['meta'].get('_yoast_wpseo_title', '')
                
                custom_payload = {
                    'post_id': post_id,
                    'meta_key': '_yoast_wpseo_metadesc', 
                    'meta_value': meta_desc
                }
                
                custom_response = requests.post(
                    custom_meta_url, 
                    headers=headers, 
                    json=custom_payload
                )
                
                if custom_response.status_code in [200, 201]:
                    print("Successfully updated metadata using custom endpoint")
                    success = True
            else:
                print("Custom meta endpoint not available, skipping this method")
        except Exception as e:
            print(f"Error in Attempt 4: {e}")
    
    # Attempt 5: Try to use admin-ajax.php as last resort
    if not success:
        try:
            print("Attempt 5: Using admin-ajax.php as last resort")
            
            # Extract domain from WP URL
            domain_match = re.search(r'(https?://[^/]+)', wp_url)
            if domain_match:
                domain = domain_match.group(1)
                admin_ajax_url = f"{domain}/wp-admin/admin-ajax.php"
                
                # Create nonce headers (these would typically come from the WordPress admin area)
                # This is a very fallback approach that likely won't work without proper nonce
                ajax_headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                
                # Try to use admin-ajax to update a meta field
                meta_desc = post_data['meta'].get('_yoast_wpseo_metadesc', '')
                
                ajax_data = {
                    'action': 'update_post_meta',
                    'post_id': post_id,
                    'meta_key': '_yoast_wpseo_metadesc',
                    'meta_value': meta_desc
                }
                
                ajax_response = requests.post(
                    admin_ajax_url,
                    headers=ajax_headers,
                    data=ajax_data
                )
                
                if ajax_response.status_code == 200:
                    try:
                        ajax_result = ajax_response.json()
                        if ajax_result.get('success'):
                            print("Successfully updated metadata using admin-ajax.php")
                            success = True
                    except:
                        # Response might not be JSON
                        if "success" in ajax_response.text.lower():
                            print("Possibly updated metadata using admin-ajax.php")
                            success = True
            else:
                print("Could not extract domain for admin-ajax.php approach")
        except Exception as e:
            print(f"Error in Attempt 5: {e}")
    
    # If all automated methods have failed, provide SQL and PHP instructions
    if not success:
        _provide_manual_update_instructions(post_id, post_data)
    
    return success

def _provide_manual_update_instructions(post_id, post_data):
    """Provide manual instructions for updating Yoast SEO metadata.
    
    Args:
        post_id (int): ID of the post
        post_data (dict): Dictionary containing meta data
    """
    print("\nAll automated methods to update metadata failed. Here are manual instructions:")
    
    # SQL queries to manually update meta fields
    print("\nSQL queries to update metadata:")
    metadesc_value = post_data['meta'].get('_yoast_wpseo_metadesc', '').replace("'", "''")
    focuskw_value = post_data['meta'].get('_yoast_wpseo_focuskw', '').replace("'", "''")
    title_value = post_data['meta'].get('_yoast_wpseo_title', '').replace("'", "''")
    
    print(f"INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ({post_id}, '_yoast_wpseo_metadesc', '{metadesc_value}');")
    print(f"INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ({post_id}, '_yoast_wpseo_focuskw', '{focuskw_value}');")
    print(f"INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ({post_id}, '_yoast_wpseo_title', '{title_value}');")
    print("-- Or, to update existing values:")
    print(f"UPDATE wp_postmeta SET meta_value = '{metadesc_value}' WHERE post_id = {post_id} AND meta_key = '_yoast_wpseo_metadesc';")
    print(f"UPDATE wp_postmeta SET meta_value = '{focuskw_value}' WHERE post_id = {post_id} AND meta_key = '_yoast_wpseo_focuskw';")
    print(f"UPDATE wp_postmeta SET meta_value = '{title_value}' WHERE post_id = {post_id} AND meta_key = '_yoast_wpseo_title';")
    print("-- Note: Your WordPress database table prefix might not be 'wp_'. Check your wp-config.php file.")
    
    # PHP script to update meta fields
    print("\nOr you can use this PHP script to update Yoast SEO meta:")
    php_metadesc = post_data['meta'].get('_yoast_wpseo_metadesc', '').replace("'", "\\'")
    php_focuskw = post_data['meta'].get('_yoast_wpseo_focuskw', '').replace("'", "\\'")
    php_title = post_data['meta'].get('_yoast_wpseo_title', '').replace("'", "\\'")
    
    php_script = f"""<?php
// WordPress Yoast SEO Meta Updater
// -----------------------------------
// Save this file as update-yoast-meta.php in your WordPress root directory
// Run it by visiting: https://your-site.com/update-yoast-meta.php

// Security check - comment out after testing
if (!isset($_GET['run'])) {{
    echo "Add ?run=1 to the URL to execute this script.";
    exit;
}}

// Load WordPress
require_once('wp-load.php');

// Post ID to update
$post_id = {post_id};

// Update Yoast SEO meta fields
update_post_meta($post_id, '_yoast_wpseo_metadesc', '{php_metadesc}');
update_post_meta($post_id, '_yoast_wpseo_focuskw', '{php_focuskw}');
update_post_meta($post_id, '_yoast_wpseo_title', '{php_title}');

// Additional fields
update_post_meta($post_id, '_yoast_wpseo_opengraph-title', '{php_title}');
update_post_meta($post_id, '_yoast_wpseo_opengraph-description', '{php_metadesc}');
update_post_meta($post_id, '_yoast_wpseo_twitter-title', '{php_title}');
update_post_meta($post_id, '_yoast_wpseo_twitter-description', '{php_metadesc}');

// Output results
echo "<h1>Yoast SEO Meta Update</h1>";
echo "<p>Updated Yoast SEO meta for post ID: $post_id</p>";
echo "<ul>";
echo "<li>Meta Description: {php_metadesc}</li>";
echo "<li>Focus Keyphrase: {php_focuskw}</li>";
echo "<li>SEO Title: {php_title}</li>";
echo "</ul>";

// Remove this file after use for security
// unlink(__FILE__);
?>"""
    
    print(php_script)
    
    # WordPress admin instructions
    print("\nTo update Yoast SEO fields manually in WordPress admin:")
    print(f"1. Go to: /wp-admin/post.php?post={post_id}&action=edit")
    print("2. Scroll down to the Yoast SEO section")
    print(f"3. Set Focus Keyphrase: {post_data['meta'].get('_yoast_wpseo_focuskw', '')}")
    print(f"4. Set Meta Description: {post_data['meta'].get('_yoast_wpseo_metadesc', '')}")
    print("5. Click Update to save changes")

# Add this new function to check metadata status after posting
def verify_meta_data(wp_url, post_id, headers, debug=False):
    """Verify if metadata was correctly saved by retrieving the post.
    
    Args:
        wp_url (str): WordPress site URL
        post_id (int): ID of the post to verify
        headers (dict): Headers to use for authentication
        debug (bool): Whether to print debug information
        
    Returns:
        bool: True if metadata appears to be set, False otherwise
    """
    try:
        # Get the post to check metadata
        get_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        get_response = requests.get(get_url, headers=headers)
        
        if get_response.status_code == 200:
            post_data = get_response.json()
            
            # Check if post has meta data
            if 'meta' in post_data:
                yoast_fields = [k for k in post_data['meta'] if k.startswith('_yoast')]
                
                if debug:
                    print("\nVerifying metadata in post:")
                    for key in yoast_fields:
                        value = post_data['meta'][key]
                        print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
                
                return len(yoast_fields) > 0
            else:
                print("Post does not contain 'meta' field in response")
                return False
        else:
            print(f"Failed to retrieve post: HTTP {get_response.status_code}")
            return False
    except Exception as e:
        print(f"Error verifying metadata: {e}")
        return False 