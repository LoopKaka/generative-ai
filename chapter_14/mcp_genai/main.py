from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Genai_python")

@mcp.tool()
def weather_tool(city: str):
    """
        Takes city name as input and finds the temerature of the city and returns
    """
    # TODO call weather external API
    if city.lower() == 'manali':
        return "-1 degree celcius"
    if city.lower() == "mumbai":
        return "32 degree celcius"
    
    return "Temperature not found for the given city"

# Todo application

todo_list = []

@mcp.tool()
def create_task(task: str):
    """
    Add a todo task to todo_list with the following structure:
    { "todo": str, "is_done": bool }
    Returns a success message.
    """
    todo_list.append({"todo": task, "is_done": False})

    return "Sucessfull"

@mcp.tool()
def display():
    """
        Display Todo table in below format:

        if is_done == True, use ✅ else use ❌

        Your TODO Task: \n

        id | Task | Status
        ------------------
        1  | abc  | ✅
        2  | xyz  | ❌
    """
    return todo_list

@mcp.tool()
def mark_completed(index: int):
    """
        Takes a task_index (1-based index) and marks is_done = True.
        Returns a success message.
    """
    todo_list[index-1]["is_done"] = True

@mcp.tool()
def clear_todo():
    """
        Clears the todo_list and returns a success message.
    """
    global todo_list
    todo_list = []
    return "All todos cleared"


def main():
    print("Hello from mcp-genai!")


if __name__ == "__main__":
    main()
