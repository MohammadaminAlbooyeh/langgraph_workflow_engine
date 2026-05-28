const initialState = {
  workflows: [],
  currentWorkflow: null,
  loading: false,
  error: null,
};

export default function workflowReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_WORKFLOWS':
      return { ...state, workflows: action.payload, loading: false };
    case 'SET_CURRENT_WORKFLOW':
      return { ...state, currentWorkflow: action.payload };
    case 'ADD_WORKFLOW':
      return { ...state, workflows: [...state.workflows, action.payload] };
    case 'UPDATE_WORKFLOW':
      return {
        ...state,
        workflows: state.workflows.map(w => w.id === action.payload.id ? action.payload : w),
        currentWorkflow: state.currentWorkflow?.id === action.payload.id ? action.payload : state.currentWorkflow,
      };
    case 'DELETE_WORKFLOW':
      return {
        ...state,
        workflows: state.workflows.filter(w => w.id !== action.payload),
        currentWorkflow: state.currentWorkflow?.id === action.payload ? null : state.currentWorkflow,
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}
