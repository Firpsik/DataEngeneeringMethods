"""
Module for generating synthetic data with anomalies
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('ru_RU')
Faker.seed(42)
np.random.seed(42)
random.seed(42)


def get_dataset(num_records=1000):
    """
    Generate synthetic dataset with intentional anomalies
    
    The dataset contains:
    - Type 1 SCD (Slowly Changing Dimension) historicity
    - 10 fields: 5 categorical, 5 quantitative
    - Intentional anomalies: nulls, duplicates, invalid dates, negative values, etc.
    
    Args:
        num_records (int): Number of records to generate
        
    Returns:
        pd.DataFrame: DataFrame with synthetic data containing anomalies
    """
    
    data = []
    
    for i in range(num_records):
        # Generate record with various anomalies
        
        # ID (with occasional duplicates)
        if random.random() < 0.05:  # 5% duplicates
            record_id = random.randint(1, i) if i > 0 else 1
        else:
            record_id = i + 1
        
        # Customer name (with nulls and irregular formatting)
        if random.random() < 0.1:  # 10% nulls
            customer_name = None
        elif random.random() < 0.15:  # 15% irregular formatting
            customer_name = fake.name().upper() + "  "  # Extra spaces
        else:
            customer_name = fake.name()
        
        # Product category (with typos and nulls)
        categories = ['Электроника', 'Одежда', 'Продукты', 'Мебель', 'Книги']
        if random.random() < 0.08:  # 8% nulls
            category = None
        elif random.random() < 0.12:  # 12% typos/inconsistencies
            category = random.choice(['электроника', 'ОДЕЖДА', ' Продукты ', 'мебель'])
        else:
            category = random.choice(categories)
        
        # City (with nulls and mixed case)
        if random.random() < 0.07:  # 7% nulls
            city = None
        elif random.random() < 0.1:
            city = fake.city().lower()
        else:
            city = fake.city()
        
        # Status (with invalid values)
        statuses = ['Активный', 'Неактивный', 'Приостановлен']
        if random.random() < 0.1:  # 10% invalid/null
            status = random.choice([None, 'Неизвестно', '', 'N/A'])
        else:
            status = random.choice(statuses)
        
        # Payment method (with nulls)
        payment_methods = ['Карта', 'Наличные', 'Перевод', 'Криптовалюта']
        if random.random() < 0.06:  # 6% nulls
            payment_method = None
        else:
            payment_method = random.choice(payment_methods)
        
        # Amount (with negative values and nulls)
        if random.random() < 0.05:  # 5% nulls
            amount = None
        elif random.random() < 0.08:  # 8% negative values
            amount = round(random.uniform(-1000, -10), 2)
        elif random.random() < 0.05:  # 5% extremely large values
            amount = round(random.uniform(1000000, 10000000), 2)
        else:
            amount = round(random.uniform(10, 50000), 2)
        
        # Quantity (with negative and zero values)
        if random.random() < 0.05:  # 5% nulls
            quantity = None
        elif random.random() < 0.1:  # 10% negative or zero
            quantity = random.randint(-10, 0)
        else:
            quantity = random.randint(1, 100)
        
        # Discount percentage (with invalid values)
        if random.random() < 0.07:  # 7% nulls
            discount = None
        elif random.random() < 0.1:  # 10% invalid (>100% or negative)
            discount = round(random.uniform(-50, 150), 2)
        else:
            discount = round(random.uniform(0, 30), 2)
        
        # Transaction date (with nulls and future dates)
        if random.random() < 0.06:  # 6% nulls
            transaction_date = None
        elif random.random() < 0.08:  # 8% future dates
            transaction_date = fake.date_between(start_date='+1d', end_date='+2y')
        else:
            transaction_date = fake.date_between(start_date='-2y', end_date='today')
        
        # Rating (with out-of-range values)
        if random.random() < 0.08:  # 8% nulls
            rating = None
        elif random.random() < 0.12:  # 12% out of range (should be 1-5)
            rating = round(random.uniform(-1, 10), 1)
        else:
            rating = round(random.uniform(1, 5), 1)
        
        data.append({
            'record_id': record_id,
            'customer_name': customer_name,
            'product_category': category,
            'city': city,
            'status': status,
            'payment_method': payment_method,
            'amount': amount,
            'quantity': quantity,
            'discount_percent': discount,
            'transaction_date': transaction_date,
            'rating': rating
        })
    
    df = pd.DataFrame(data)
    
    print(f"Generated {len(df)} records with intentional anomalies:")
    print(f"  - Null values: {df.isnull().sum().sum()}")
    print(f"  - Duplicate IDs: {df['record_id'].duplicated().sum()}")
    print(f"  - Negative amounts: {(df['amount'] < 0).sum() if df['amount'].notna().any() else 0}")
    print(f"  - Invalid ratings: {((df['rating'] < 1) | (df['rating'] > 5)).sum() if df['rating'].notna().any() else 0}")
    
    return df
