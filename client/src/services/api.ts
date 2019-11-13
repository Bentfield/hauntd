import axios, { AxiosRequestConfig } from 'axios';

const config : AxiosRequestConfig = {
  baseURL: 'https://zdllkm9js8.execute-api.us-east-1.amazonaws.com/api',
};

const httpClient = axios.create(config);

export default httpClient;
