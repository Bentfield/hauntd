import axios, { AxiosRequestConfig } from 'axios';

const config : AxiosRequestConfig = {
  baseURL: process.env.VUE_APP_API,
};

const httpClient = axios.create(config);

export default httpClient;
