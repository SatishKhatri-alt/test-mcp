from motor.motor_asyncio import AsyncIOMotorClient

from fastmcp import FastMCP
from bson import ObjectId

# ---------------- MongoDB setup ----------------
MONGO_DB_URL = "mongodb+srv://satish:satish9@cluster0.3u6xf0v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "Udharo-db"

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[DATABASE_NAME]

# ---------------- FastMCP setup ----------------
mcp = FastMCP(name="Expense-Manager")


# ---------------- MCP Tools ----------------
@mcp.tool
async def add_expense(amount: int, category: str, date: str, note: str):
    """
    Add a new expense to the MongoDB collection.

    Returns:
        dict: Inserted document ID.
    """
    expenses = {
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    result = await db.expense.insert_one(expenses)
    return {"inserted_id": str(result.inserted_id)}

@mcp.tool
async def get_expense():
    """
    Retrieve all expenses, sorted by newest first.

    Returns:
        list: List of expense documents.
    """
    cursor = db.expense.find().sort("_id", -1)
    return await cursor.to_list(length=None)

@mcp.tool
async def delete_expense(id: str):
    """
    Delete an expense by MongoDB ObjectId.

    Args:
        id (str): MongoDB ObjectId as string.

    Returns:
        dict: Number of documents deleted.
    """
    result = await db.expense.delete_one({"_id": ObjectId(id)})
    return {"deleted_count": result.deleted_count}

# ---------------- Run MCP ----------------
if __name__ == "__main__":
    mcp.run(transport='http',host='0.0.0.0',port=8000)
