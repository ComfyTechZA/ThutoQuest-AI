// Custom hooks for dashboard functionality

import { useState, useEffect } from 'react';

export const useLocalStorage = (key, defaultValue) => {
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}"`, error);
      return defaultValue;
    }
  });

  const setStoredValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(value) : value;
      setValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}"`, error);
    }
  };

  return [value, setStoredValue];
};

// Prefetch data before render
export const usePrefetch = (fetchFn, deps = []) => {
  useEffect(() => {
    fetchFn();
  }, deps);
};

// Debounced values for search/filter
export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};

// Intersection observer for lazy loading
export const useIntersectionObserver = (ref, options = {}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
        observer.unobserve(entry.target);
      }
    }, options);

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [ref, options]);

  return isVisible;
};

// Analytics tracking (placeholder)
export const useAnalytics = () => {
  const trackEvent = (event, data) => {
    if (import.meta.env.VITE_ENABLE_ANALYTICS) {
      console.log(`📊 Analytics Event: ${event}`, data);
    }
  };

  return { trackEvent };
};
