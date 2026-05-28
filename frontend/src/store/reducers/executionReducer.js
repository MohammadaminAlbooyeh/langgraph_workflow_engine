const initialState = {
  executions: [],
  currentExecution: null,
  loading: false,
  error: null,
};

export default function executionReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_EXECUTIONS':
      return { ...state, executions: action.payload, loading: false };
    case 'SET_CURRENT_EXECUTION':
      return { ...state, currentExecution: action.payload };
    case 'ADD_EXECUTION':
      return { ...state, executions: [...state.executions, action.payload] };
    case 'UPDATE_EXECUTION':
      return {
        ...state,
        executions: state.executions.map(e => e.id === action.payload.id ? action.payload : e),
        currentExecution: state.currentExecution?.id === action.payload.id ? action.payload : state.currentExecution,
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}
