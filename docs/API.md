# API Documentation for Galactic-Currency

## Overview

The Galactic-Currency API provides a set of endpoints for interacting with the Galactic-Currency blockchain. It allows developers to integrate with the system, manage transactions, and access various functionalities such as wallet management and smart contract interactions.

## Base URL

[https://api.galacticcurrency.example.com/v1](https://api.galacticcurrency.example.com/v1) 


## Authentication

All API requests require authentication via an API key. You can obtain your API key by registering on our platform.

### Authentication Header

Include the following header in your requests:

```
Authorization: Bearer YOUR_API_KEY
```


## Endpoints

### 1. Get Wallet Balance

- **Endpoint**: `/wallet/balance`
- **Method**: `GET`
- **Description**: Retrieve the balance of a specified wallet.

#### Request

- **GET** /wallet/balance?address=YOUR_WALLET_ADDRESS

- 
#### Query Parameters

| Parameter | Type   | Description                     |
|-----------|--------|---------------------------------|
| address   | string | The wallet address to check.    |

#### Response

```json
1 {
2   "address": "YOUR_WALLET_ADDRESS",
3   "balance": "100.00",
4   "currency": "GALC"
5 }
```

### 2. Create Transaction
- **Endpoint**: /transactions/create
- **Method**: POST
- **Description**: Create a new transaction.

**Request**
- **POST** /transactions/create
- **Request Body**
```json
1 {
2   "from": "SENDER_WALLET_ADDRESS",
3   "to": "RECIPIENT_WALLET_ADDRESS",
4   "amount": "10.00",
5   "currency": "GALC"
6 }
```

**Response**
```json
1 {
2   "transaction_id": "TRANSACTION_ID",
3   "status": "pending"
4 }
```

### 3. Get Transaction Status
- **Endpoint**: /transactions/status
- **Method**: GET
- **Description**: Retrieve the status of a specific transaction.

**Request**
- **GET** /transactions/status?transaction_id=TRANSACTION_ID
- **Query Parameters**
**Parameter	Type	Description**
transaction_id	string	The ID of the transaction.

**Response**

```json
1 {
2   "transaction_id": "TRANSACTION_ID",
3   "status": "completed",
4   "timestamp": "2023-10-01T12:00:00Z"
5 }
```

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of a request. Below are some common error responses:

**Status Code	Description**

400	Bad Request - Invalid parameters

401	Unauthorized - Invalid API key

404	Not Found - Resource not found

500	Internal Server Error


### Error Response Format
```json
1 {
2   "error": {
3     "code": "ERROR_CODE",
4     "message": "Error message describing the issue."
5   }
6 }
```

### Rate Limiting
To ensure fair usage of the API, rate limits are applied. Each API key is limited to 100 requests per minute. Exceeding this limit will result in a 429 Too Many Requests response.

# Conclusion
For further information or support, please refer to our documentation or contact our support team.
