import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { executionApi } from '../services/execution_api';
import { setExecutions, setCurrentExecution } from '../store/actions/executionActions';
import { selectAllExecutions, selectCurrentExecution } from '../store/selectors/workflowSelectors';
import ExecutionMonitor from '../components/ExecutionMonitor';
import ExecutionTimeline from '../components/ExecutionTimeline';
import { Play, Pause, XCircle, RotateCcw } from 'lucide-react';
import { formatDate } from '../utils/formatters';

export default function ExecutionPage() {
  const dispatch = useDispatch();
  const executions = useSelector(selectAllExecutions);
  const currentExecution = useSelector(selectCurrentExecution);

  useEffect(() => {
    executionApi.list().then(({ data }) => dispatch(setExecutions(data)));
  }, [dispatch]);

  const handleCancel = async (id) => {
    const { data } = await executionApi.cancel(id);
    if (data) {
      const updated = await executionApi.get(id);
      dispatch(setCurrentExecution(updated.data));
    }
  };

  const handlePause = async (id) => {
    const { data } = await executionApi.pause(id);
    if (data) {
      const updated = await executionApi.get(id);
      dispatch(setCurrentExecution(updated.data));
    }
  };

  const handleResume = async (id) => {
    const { data } = await executionApi.resume(id);
    if (data) {
      const updated = await executionApi.get(id);
      dispatch(setCurrentExecution(updated.data));
    }
  };

  return (
    <div className="flex gap-6 h-full">
      <div className="flex-1">
        <h2 className="text-2xl font-bold text-white mb-6">Executions</h2>
        {executions.length === 0 ? (
          <div className="bg-slate-800 rounded-lg border border-slate-700 p-12 text-center">
            <p className="text-slate-400">No executions yet. Run a workflow to see results here.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {executions.map(ex => (
              <div key={ex.id}
                onClick={() => dispatch(setCurrentExecution(ex))}
                className={`bg-slate-800 rounded-lg border p-4 cursor-pointer transition-colors ${
                  currentExecution?.id === ex.id ? 'border-blue-500' : 'border-slate-700 hover:border-slate-600'
                }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white font-medium">{ex.workflow_id}</p>
                    <div className="flex items-center gap-3 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded capitalize ${
                        ex.status === 'completed' ? 'bg-green-900/30 text-green-400' :
                        ex.status === 'failed' ? 'bg-red-900/30 text-red-400' :
                        ex.status === 'running' ? 'bg-blue-900/30 text-blue-400' :
                        'bg-slate-700 text-slate-300'
                      }`}>{ex.status}</span>
                      <span className="text-xs text-slate-500">{formatDate(ex.started_at)}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {ex.status === 'running' && (
                      <>
                        <button onClick={(e) => { e.stopPropagation(); handlePause(ex.id); }}
                          className="p-1.5 text-yellow-400 hover:bg-slate-700 rounded">
                          <Pause size={14} />
                        </button>
                        <button onClick={(e) => { e.stopPropagation(); handleCancel(ex.id); }}
                          className="p-1.5 text-red-400 hover:bg-slate-700 rounded">
                          <XCircle size={14} />
                        </button>
                      </>
                    )}
                    {ex.status === 'paused' && (
                      <button onClick={(e) => { e.stopPropagation(); handleResume(ex.id); }}
                        className="p-1.5 text-green-400 hover:bg-slate-700 rounded">
                        <Play size={14} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="w-80 flex-shrink-0 space-y-4">
        <ExecutionMonitor execution={currentExecution} />
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Node Results</h3>
          <ExecutionTimeline nodeResults={currentExecution?.node_results} />
        </div>
      </div>
    </div>
  );
}
