#!/usr/bin/env python3
"""
Generate synthetic test data for benchmark
"""

import json
from pathlib import Path
import random
from datetime import datetime, timedelta

def generate_news_article():
    """Generate sample news article"""
    return """Breaking: Tech Giant Announces Major AI Breakthrough

SAN FRANCISCO - In a landmark announcement today, TechCorp unveiled its latest artificial intelligence system, claiming significant advances in natural language understanding and reasoning capabilities.

The new system, dubbed "Nexus-7", demonstrates improved performance across multiple benchmarks, including a 40% reduction in hallucination rates and enhanced contextual awareness. CEO Jane Smith stated, "This represents a fundamental shift in how AI systems process and understand human language."

Industry analysts predict the technology could impact sectors ranging from healthcare to education, with potential applications in medical diagnosis, personalized learning, and automated customer service.

However, critics raise concerns about data privacy and the environmental cost of training such large models. Dr. Robert Chen from the AI Ethics Institute warns, "We must balance innovation with responsible development practices."

The company plans to release a limited beta version to select partners next quarter, with broader availability expected by year-end."""

def generate_history_text():
    """Generate sample historical text"""
    return """The Industrial Revolution: A Timeline of Change

The Industrial Revolution, spanning from 1760 to 1840, fundamentally transformed human society through mechanization and technological innovation.

In 1764, James Hargreaves invented the spinning jenny, revolutionizing textile production and enabling a single worker to operate multiple spindles simultaneously. This innovation marked the beginning of mass manufacturing.

The year 1769 saw James Watt's improvement of the steam engine, providing a reliable power source that would drive factories and transportation for decades. This development was crucial for industrial expansion.

By 1825, the Stockton and Darlington Railway opened, becoming the world's first public railway to use steam locomotives. This breakthrough in transportation enabled rapid movement of goods and people, connecting markets and accelerating economic growth.

The Factory Act of 1833 represented a significant social reform, limiting child labor and establishing basic workplace protections. This legislation acknowledged the human cost of industrialization and set precedents for labor rights.

These developments collectively reshaped economies, urbanized populations, and established the foundation for modern industrial society."""

def generate_tech_doc():
    """Generate sample technical documentation"""
    return """# User Management API Documentation

## Overview
The User Management API provides endpoints for creating, reading, updating, and deleting user accounts in the system. All endpoints require authentication via Bearer token.

## Base URL
```
https://api.example.com/v1
```

## Authentication
Include your API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### GET /users
Retrieve a list of users with optional filtering and pagination.

**Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Results per page (default: 20, max: 100)
- `role` (string, optional): Filter by user role (admin, user, guest)
- `status` (string, optional): Filter by status (active, inactive, suspended)

**Response:**
```json
{
  "users": [...],
  "total": 150,
  "page": 1,
  "limit": 20
}
```

### POST /users
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "password": "secure_password"
}
```

**Response:** Returns the created user object with generated ID.

### GET /users/{id}
Retrieve a specific user by ID.

**Parameters:**
- `id` (string, required): User ID

**Response:** Returns user object or 404 if not found.

### PUT /users/{id}
Update an existing user.

**Request Body:** Partial user object with fields to update.

**Response:** Returns updated user object.

### DELETE /users/{id}
Delete a user account.

**Response:** 204 No Content on success.

## Rate Limits
- 1000 requests per hour per API key
- 100 requests per minute per IP address

## Error Codes
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error"""

def generate_sales_csv():
    """Generate sample sales CSV"""
    rows = ["id,date,amount,region,product"]
    for i in range(1, 51):
        date = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        amount = random.randint(5000, 50000)
        region = random.choice(["North", "South", "East", "West"])
        product = random.choice(["Widget A", "Widget B", "Gadget X", "Gadget Y"])
        rows.append(f"{i},{date},{amount},{region},{product}")
    return "\n".join(rows)

def generate_contract():
    """Generate sample contract"""
    return """SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of 2025-01-15 ("Effective Date") by and between:

PARTY A: TechCorp Solutions Inc., a Delaware corporation with principal offices at 123 Innovation Drive, San Francisco, CA 94105 ("Provider")

PARTY B: Global Enterprises LLC, a California limited liability company with principal offices at 456 Business Plaza, Los Angeles, CA 90012 ("Client")

1. TERM
This Agreement shall commence on 2025-02-01 and continue until 2026-01-31, unless earlier terminated as provided herein ("Term").

2. SERVICES
Provider agrees to provide software development and consulting services as detailed in Exhibit A, including but not limited to: system architecture design, code development, testing, and deployment support.

3. COMPENSATION
Client shall pay Provider a monthly fee of $50,000, payable within 30 days of invoice receipt. Additional services beyond the scope defined in Exhibit A shall be billed at $200 per hour.

4. TERMINATION
Either party may terminate this Agreement with 60 days written notice. In the event of material breach, the non-breaching party may terminate immediately upon written notice if the breach is not cured within 30 days.

5. TERMINATION CLAUSE
Upon termination, Provider shall deliver all work product completed to date, and Client shall pay for all services rendered through the termination date. Any prepaid fees for services not yet rendered shall be refunded on a pro-rata basis within 30 days of termination.

6. CONFIDENTIALITY
Both parties agree to maintain confidentiality of proprietary information disclosed during the Term and for 3 years thereafter.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

TechCorp Solutions Inc.          Global Enterprises LLC
By: Sarah Johnson, CEO           By: Michael Chen, COO
Date: 2025-01-15                 Date: 2025-01-15"""

def generate_all_data(output_dir: Path):
    """Generate all test data files"""
    output_dir.mkdir(exist_ok=True)
    
    files = {
        "news_article_1.txt": generate_news_article(),
        "history_text_1.txt": generate_history_text(),
        "tech_doc_1.txt": generate_tech_doc(),
        "sales_2025.csv": generate_sales_csv(),
        "contract_1.txt": generate_contract(),
    }
    
    for filename, content in files.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Generated: {filepath}")
    
    print(f"\n✅ Generated {len(files)} test data files in {output_dir}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic test data")
    parser.add_argument("--output-dir", default="data", help="Output directory")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    generate_all_data(output_dir)

if __name__ == "__main__":
    main()
