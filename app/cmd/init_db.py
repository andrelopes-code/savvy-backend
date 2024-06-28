import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.postgres import async_session
from app.models.category import Category


async def init_db():
    async with async_session() as session:
        await add_default_categories(session)


async def add_default_categories(session: AsyncSession):
    categories = [  # noqa
        {
            'name': 'Food',
            'description': 'Expenses for groceries, dining out, snacks, and beverages.',  # noqa
        },
        {
            'name': 'Transport',
            'description': 'Expenses for public transportation, fuel, car maintenance, and parking.',  # noqa
        },
        {
            'name': 'Health',
            'description': 'Expenses for medical bills, medications, health insurance, and wellness.',  # noqa
        },
        {
            'name': 'Housing',
            'description': 'Expenses for rent, mortgage, property taxes, and home maintenance.',  # noqa
        },
        {
            'name': 'Utilities',
            'description': 'Expenses for electricity, water, gas, and internet bills.',  # noqa
        },
        {
            'name': 'Entertainment',
            'description': 'Expenses for movies, concerts, sports events, and recreational activities.',  # noqa
        },
        {
            'name': 'Education',
            'description': 'Expenses for tuition, books, courses, and school supplies.',  # noqa
        },
        {
            'name': 'Insurance',
            'description': 'Expenses for various insurance premiums such as health, auto, home, and life insurance.',  # noqa
        },
        {
            'name': 'Clothing',
            'description': 'Expenses for apparel, footwear, and accessories.',
        },
        {
            'name': 'Personal Care',
            'description': 'Expenses for grooming, toiletries, haircuts, and beauty products.',  # noqa
        },
        {
            'name': 'Subscriptions',
            'description': 'Expenses for magazine, newspaper, streaming services, and other subscriptions.',  # noqa
        },
        {
            'name': 'Gifts',
            'description': 'Expenses for gifts for family, friends, and special occasions.',  # noqa
        },
        {
            'name': 'Charity',
            'description': 'Expenses for donations to charitable organizations and causes.',  # noqa
        },
        {
            'name': 'Travel',
            'description': 'Expenses for flights, hotels, vacation packages, and travel-related costs.',  # noqa
        },
        {
            'name': 'Dining Out',
            'description': 'Expenses for eating out at restaurants and cafes.',
        },
        {
            'name': 'Fitness',
            'description': 'Expenses for gym memberships, fitness classes, and sports equipment.',  # noqa
        },
        {
            'name': 'Childcare',
            'description': 'Expenses for daycare, babysitting, and child-related activities.',  # noqa
        },
        {
            'name': 'Pets',
            'description': 'Expenses for pet food, veterinary care, grooming, and pet supplies.',  # noqa
        },
        {
            'name': 'Loans',
            'description': 'Expenses for loan repayments, including student loans, personal loans, and credit cards.',  # noqa
        },
        {
            'name': 'Savings',
            'description': 'Money set aside for savings, investments, and emergency funds.',  # noqa
        },
        {
            'name': 'Business Expenses',
            'description': 'Expenses related to running a business, including office supplies and services.',  # noqa
        },
        {
            'name': 'Miscellaneous',
            'description': "Expenses that don't fit into other categories, including unforeseen costs.",  # noqa
        },
        {
            'name': 'Home Improvement',
            'description': 'Expenses for home renovation and improvement projects.',  # noqa
        },
        {
            'name': 'Alcohol & Tobacco',
            'description': 'Expenses for alcoholic beverages and tobacco products.',  # noqa
        },
        {
            'name': 'Hobbies',
            'description': 'Expenses for hobbies, crafts, and leisure activities.',  # noqa
        },
    ]

    existing_categories = await session.execute(select(Category))
    existing_categories = existing_categories.scalars().all()

    if not existing_categories:
        session.add_all([
            Category(name=cat['name'], description=cat['description'])
            for cat in categories
        ])
        await session.commit()


if __name__ == '__main__':
    asyncio.run(init_db())
