import axios, { AxiosRequestConfig } from 'axios';

const config : AxiosRequestConfig = {
  baseURL: 'https://5ijvyvethe.execute-api.us-east-1.amazonaws.com/dev',
};

const httpClient = axios.create(config);

export default httpClient;
