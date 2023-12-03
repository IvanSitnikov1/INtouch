import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json'
  }
});

let isRefreshing = false;
let failedRequestsQueue = [];

const processQueue = (error, token = null) => {
  failedRequestsQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedRequestsQueue = [];
};

async function refreshTokens() {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    throw new Error("No refresh token available");
  }
  const response = await API.post('token/refresh/', { refresh: refreshToken });
  const { access: newAccessToken, refresh: newRefreshToken } = response.data;
  localStorage.setItem('accessToken', newAccessToken);
  localStorage.setItem('refreshToken', newRefreshToken);
  API.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
  return newAccessToken;
}

API.interceptors.request.use(
  config => {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

API.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function(resolve, reject) {
          failedRequestsQueue.push({ resolve, reject });
        })
        .then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return API(originalRequest);
        })
        .catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newAccessToken = await refreshTokens();
        processQueue(null, newAccessToken);
        return API(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default API;
