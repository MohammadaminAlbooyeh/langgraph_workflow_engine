import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import workflowReducer from './reducers/workflowReducer';
import executionReducer from './reducers/executionReducer';
import agentReducer from './reducers/agentReducer';
import monitoringReducer from './reducers/monitoringReducer';

const rootReducer = combineReducers({
  workflows: workflowReducer,
  executions: executionReducer,
  agents: agentReducer,
  monitoring: monitoringReducer,
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(rootReducer, composeEnhancers(applyMiddleware()));

export default store;
