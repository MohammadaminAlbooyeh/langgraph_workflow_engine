const initialState = {
  metrics: null,
  summary: null,
  loading: false,
  error: null,
};

export default function monitoringReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_METRICS':
      return { ...state, metrics: action.payload, loading: false };
    case 'SET_SUMMARY':
      return { ...state, summary: action.payload, loading: false };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}
