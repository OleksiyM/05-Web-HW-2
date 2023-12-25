# Exchange Rate WebSocket Chat Server

This project is a WebSocket chat server that retrieves exchange rate data from PrivatBank and displays it in a user-friendly chat interface.

## Features

* **Real-time exchange rate updates:** The server fetches data directly from PrivatBank's API, ensuring up-to-date information.
* **Customizable data retrieval:** Users can specify the number of archive days (up to 10) and currencies to retrieve using chat commands.
* **Interactive chat interface:** Users can send messages and receive exchange rate updates seamlessly.
* **Clean and organized code:** The project adheres to best practices for readability and maintainability.

## Getting Started

1. Clone this repository
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python main.py
   ```
4. Open `index.html` in your web browser to access the chat interface.

## Usage

1. Connect to the WebSocket chat server using the provided URL in `index.html`.
2. Use the following command to retrieve exchange rate data:
   ```
   exchange [days] [all]
   
   - `days`: Optional argument to specify the number of days of data to retrieve (default is 0, meaning current day).
   - `all`: Optional argument to retrieve data for all supported currencies (default is base currencies: EUR, USD).

## Technologies Used

* Python
* WebSockets
* aiohttp
* asyncio
* PrivatBank API

## Contributing

We welcome contributions! Please feel free to open issues or pull requests to suggest improvements or fix any bugs.

