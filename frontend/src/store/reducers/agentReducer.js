const initialState = {
  agents: [],
  loading: false,
  error: null,
};

export default function agentReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_AGENTS':
      return { ...state, agents: action.payload, loading: false };
    case 'ADD_AGENT':
      return { ...state, agents: [...state.agents, action.payload] };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}
