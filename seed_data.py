#!/usr/bin/env python3
"""
Seed script to populate Firestore with test data for the Ad Campaign Directory.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os

# Initialize Firebase Admin SDK with explicit project
PROJECT_ID = "contentplan-479308"

try:
    app = firebase_admin.get_app()
except ValueError:
    # Initialize with explicit project ID
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': PROJECT_ID,
    })
    print(f"✓ Initialized Firebase Admin SDK for project: {PROJECT_ID}")

db = firestore.client()
print(f"✓ Connected to Firestore")

USER_ID = "0guMxa93fefiqmiMDeRkgoRWb3Y2"

def create_user_document():
    """Create a user document if it doesn't exist."""
    user_ref = db.collection('users').document(USER_ID)
    user_ref.set({
        'email': 'test@example.com',
        'display_name': 'Test User',
        'role': 'client',
        'created_at': firestore.SERVER_TIMESTAMP,
        'last_login': firestore.SERVER_TIMESTAMP
    }, merge=True)
    print(f"✓ Created/Updated user: {USER_ID}")

def create_content_plans():
    """Create test content plans."""
    plans_data = [
        {
            'name': 'Spring Campaign 2024',
            'status': 'Active',
            'client_ref': db.collection('users').document(USER_ID),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'enabled_statuses': ['Draft', 'In Review', 'Approved', 'Live', 'Paused'],
            'enabled_platforms': ['meta', 'tiktok', 'snapchat'],
            'enabled_tags': [
                {'category': 'Funnel step', 'options': ['Awareness', 'Consideration', 'Conversion']},
                {'category': 'Audience', 'options': ['B2B', 'B2C', 'Mixed']},
                {'category': 'Product', 'options': ['Shoes', 'Apparel', 'Accessories']}
            ]
        },
        {
            'name': 'Black Friday 2024',
            'status': 'Active',
            'client_ref': db.collection('users').document(USER_ID),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'enabled_statuses': ['Draft', 'Live', 'Ended'],
            'enabled_platforms': ['meta', 'youtube', 'pinterest'],
            'enabled_tags': [
                {'category': 'Funnel step', 'options': ['Awareness', 'Conversion']},
                {'category': 'Audience', 'options': ['B2C']},
                {'category': 'Product', 'options': ['Electronics', 'Home Goods']}
            ]
        }
    ]
    
    plan_refs = []
    for plan_data in plans_data:
        plan_ref = db.collection('content_plans').document()
        plan_ref.set(plan_data)
        plan_refs.append(plan_ref)
        print(f"✓ Created content plan: {plan_data['name']} (ID: {plan_ref.id})")
    
    return plan_refs

def create_campaigns(plan_ref, plan_name):
    """Create campaigns for a content plan."""
    campaigns_data = [
        {
            'name': 'Always On',
            'type': 'always_on',
            'status': 'active',
            'budget': 5000
        },
        {
            'name': f'{plan_name} - Launch Week',
            'type': 'campaign',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=7),
            'status': 'active',
            'budget': 10000
        },
        {
            'name': f'{plan_name} - Retargeting',
            'type': 'campaign',
            'start_date': datetime.now() + timedelta(days=8),
            'end_date': datetime.now() + timedelta(days=30),
            'status': 'planned',
            'budget': 7500
        }
    ]
    
    campaign_refs = []
    for campaign_data in campaigns_data:
        campaign_ref = plan_ref.collection('campaigns').document()
        campaign_ref.set(campaign_data)
        campaign_refs.append(campaign_ref)
        print(f"  ✓ Created campaign: {campaign_data['name']} (ID: {campaign_ref.id})")
    
    return campaign_refs

def create_ads(plan_ref, campaign_refs, plan_name):
    """Create test ads for a content plan."""
    
    # Get campaign references
    always_on_ref = campaign_refs[0]
    launch_ref = campaign_refs[1]
    
    ads_data = [
        {
            'campaign_ref': always_on_ref,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'status': 'Live',
            'ad_name': 'Meta Brand Awareness - Always On',
            'img': 'https://via.placeholder.com/1200x628',
            'platform': ['meta'],
            'media_type': 'image',
            'landing_page': 'https://example.com/products',
            'assets_link': 'https://drive.google.com/example1',
            'comments': 'Performing well, keep running',
            'tags': [
                {'category': 'Funnel step', 'options': ['Awareness']},
                {'category': 'Audience', 'options': ['B2C']},
                {'category': 'Product', 'options': ['Shoes']}
            ],
            'meta_headlines': ['Step into Style', 'Premium Footwear', 'Comfort Meets Fashion'],
            'meta_preview_texts': ['Discover our new collection', 'Free shipping on orders over $50'],
            'headline': '',
            'tiktok_ad_text': '',
            'pinterest_description': '',
            'youtube_short_headline': '',
            'youtube_long_headline': ''
        },
        {
            'campaign_ref': launch_ref,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'status': 'Live',
            'ad_name': 'TikTok Product Launch Video',
            'img': 'https://via.placeholder.com/1080x1920',
            'platform': ['tiktok'],
            'media_type': 'video',
            'landing_page': 'https://example.com/new-arrivals',
            'assets_link': 'https://drive.google.com/example2',
            'comments': 'High engagement rate',
            'tags': [
                {'category': 'Funnel step', 'options': ['Consideration']},
                {'category': 'Audience', 'options': ['B2C']},
                {'category': 'Product', 'options': ['Apparel']}
            ],
            'meta_headlines': [],
            'meta_preview_texts': [],
            'headline': '',
            'tiktok_ad_text': 'New arrivals just dropped! 🔥 Shop now and get 20% off your first order. Link in bio! #fashion #style',
            'pinterest_description': '',
            'youtube_short_headline': '',
            'youtube_long_headline': ''
        },
        {
            'campaign_ref': launch_ref,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'status': 'In_Progress',
            'ad_name': 'Snapchat Story Ad - Launch',
            'img': 'https://via.placeholder.com/1080x1920',
            'platform': ['snapchat'],
            'media_type': 'video',
            'landing_page': 'https://example.com/sale',
            'assets_link': 'https://drive.google.com/example3',
            'comments': 'Waiting for approval',
            'tags': [
                {'category': 'Funnel step', 'options': ['Conversion']},
                {'category': 'Audience', 'options': ['B2C']},
                {'category': 'Product', 'options': ['Accessories']}
            ],
            'meta_headlines': [],
            'meta_preview_texts': [],
            'headline': 'Limited Time Offer - 30% Off',
            'tiktok_ad_text': '',
            'pinterest_description': '',
            'youtube_short_headline': '',
            'youtube_long_headline': ''
        },
        {
            'campaign_ref': always_on_ref,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'status': 'Live',
            'ad_name': 'Meta Carousel - Product Showcase',
            'img': 'https://via.placeholder.com/1200x628',
            'platform': ['meta'],
            'media_type': 'carousel',
            'landing_page': 'https://example.com/collections',
            'assets_link': 'https://drive.google.com/example4',
            'comments': 'Testing different headlines',
            'tags': [
                {'category': 'Funnel step', 'options': ['Consideration']},
                {'category': 'Audience', 'options': ['Mixed']},
                {'category': 'Product', 'options': ['Shoes', 'Apparel']}
            ],
            'meta_headlines': ['Shop the Collection', 'Find Your Style', 'Quality You Can Trust', 'Made for You', 'Explore Now'],
            'meta_preview_texts': ['Browse our curated selection', 'Something for everyone', 'Premium quality guaranteed'],
            'headline': '',
            'tiktok_ad_text': '',
            'pinterest_description': '',
            'youtube_short_headline': '',
            'youtube_long_headline': ''
        },
        {
            'campaign_ref': launch_ref,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'status': 'Paused',
            'ad_name': 'Meta Video - Brand Story',
            'img': 'https://via.placeholder.com/1200x628',
            'platform': ['meta'],
            'media_type': 'video',
            'landing_page': 'https://example.com/about',
            'assets_link': 'https://drive.google.com/example5',
            'comments': 'Paused for creative refresh',
            'tags': [
                {'category': 'Funnel step', 'options': ['Awareness']},
                {'category': 'Audience', 'options': ['B2B', 'B2C']},
                {'category': 'Product', 'options': ['Shoes']}
            ],
            'meta_headlines': ['Our Story', 'Crafted with Care'],
            'meta_preview_texts': ['Learn about our journey', 'Quality craftsmanship since 2020'],
            'headline': '',
            'tiktok_ad_text': '',
            'pinterest_description': '',
            'youtube_short_headline': '',
            'youtube_long_headline': ''
        }
    ]
    
    for ad_data in ads_data:
        ad_ref = plan_ref.collection('ads').document()
        ad_ref.set(ad_data)
        print(f"  ✓ Created ad: {ad_data['ad_name']} (ID: {ad_ref.id})")

def main():
    print("🌱 Starting seed process...\n")
    
    # Create user
    create_user_document()
    print()
    
    # Create content plans
    plan_refs = create_content_plans()
    print()
    
    # For each plan, create campaigns and ads
    for i, plan_ref in enumerate(plan_refs):
        plan_doc = plan_ref.get()
        plan_name = plan_doc.get('name')
        
        print(f"📋 Populating plan: {plan_name}")
        campaign_refs = create_campaigns(plan_ref, plan_name)
        create_ads(plan_ref, campaign_refs, plan_name)
        print()
    
    print("✅ Seed completed successfully!")
    print(f"\nCreated:")
    print(f"  - 1 user")
    print(f"  - {len(plan_refs)} content plans")
    print(f"  - {len(plan_refs) * 3} campaigns")
    print(f"  - {len(plan_refs) * 5} ads")

if __name__ == '__main__':
    main()
