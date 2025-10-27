// src/const/uri.js
export const API_HOST = import.meta.env.VITE_API_BASE?.replace(/\/$/, '') || 'http://127.0.0.1:8000/api';
export const API_BASE = {
  region: `${API_HOST}/regions/`,
  city: `${API_HOST}/cities/`,
  wave: `${API_HOST}/waves/`,
  survey: `${API_HOST}/surveys/`,
  question: `${API_HOST}/questions/`,
  metric: `${API_HOST}/metrics/`,
  datapoint: `${API_HOST}/datapoints/`,
  choropleth: `${API_HOST}/choropleth/`,
};
