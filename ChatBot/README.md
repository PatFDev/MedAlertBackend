### `ChatBot` Folder Documentation

The `ChatBot` folder contains all the code and utilities required for the chatbot functionality of the project. This chatbot is designed to assist with healthcare-related queries, providing intelligent responses based on user input, current medications, and conversation history.

---

## Folder Structure

```
ChatBot/
├── __init__.py      # Initializes the module
├── routes.py        # Defines Flask routes for chatbot-related endpoints
├── utils.py         # Contains utility functions to format requests and interact with OpenAI API
```

---

## Endpoints

### `/chatbot/ask`
This endpoint handles user queries, providing intelligent responses based on:
- A user message.
- A list of medications the user is currently taking.
- The conversation history for multi-turn interactions.

#### Request
- **Method**: `POST`
- **Content-Type**: `application/json`

#### JSON Body Example
```json
{
  "message": "Can I take ibuprofen with my current medications?",
  "medications": ["aspirin", "metformin"],
  "conversation": [
    {"role": "user", "content": "What should I do if I miss a dose of metformin?"},
    {"role": "assistant", "content": "If you miss a dose of metformin, take it as soon as you remember unless it’s almost time for your next dose."}
  ]
}
```

#### Response
- **Status Code**: `200 OK`
- **Response Body Example**:
```json
{
  "response": "It’s generally safe to take ibuprofen with aspirin, but there are some risks of stomach irritation or bleeding. Please consult your doctor for specific advice."
}
```

#### Error Responses
- **400 Bad Request**: If required fields are missing or improperly formatted.
  ```json
  { "error": "User message is required" }
  ```
- **500 Internal Server Error**: If there is an issue with the OpenAI API or other server-side logic.
  ```json
  { "error": "OpenAI API error: [Error Message]" }
  ```

---

## Utilities

### `utils.py`

This file contains reusable utility functions that streamline chatbot functionality.

#### Functions

1. **`format_openai_messages(developer_message, medications, conversation, user_message)`**
   - Formats the input data into a structure compatible with OpenAI's `ChatCompletion` API.
   - **Parameters**:
     - `developer_message` (str): Instruction for how the assistant should behave.
     - `medications` (list): List of the user’s current medications.
     - `conversation` (list): Previous messages in the conversation history.
     - `user_message` (str): The latest message from the user.
   - **Returns**: A formatted list of messages.

2. **`get_openai_response(messages, model="gpt-4o")`**
   - Sends a request to OpenAI’s API with the given messages and retrieves the assistant's response.
   - **Parameters**:
     - `messages` (list): The formatted input for OpenAI.
     - `model` (str): The model to use (default is `"gpt-4o"`).
   - **Returns**: The assistant’s response as a string.
   - **Raises**: Exception with the error message if the API call fails.

---

## How to Use

1. **Add the ChatBot Blueprint**:
   In your main application (`main.py`), register the blueprint:
   ```python
   from ChatBot.routes import blueprint as chatbot_blueprint
   app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')
   ```

2. **Run the Server**:
   Start the Flask application:
   ```bash
   python main.py
   ```

3. **Test the Endpoint**:
   Use a tool like `curl` or Postman to send a `POST` request to `/chatbot/ask`. Example `curl` request:
   ```bash
   curl -X POST http://127.0.0.1:5000/chatbot/ask \
   -H "Content-Type: application/json" \
   -d '{
     "message": "Can I take ibuprofen with my current medications?",
     "medications": ["aspirin", "metformin"],
     "conversation": [
       {"role": "user", "content": "What should I do if I miss a dose of metformin?"},
       {"role": "assistant", "content": "If you miss a dose of metformin, take it as soon as you remember unless it’s almost time for your next dose."}
     ]
   }'
   ```

---

## Notes
- Make sure to include your API key

---

