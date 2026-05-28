export const formatDuration = (ms) => {
  if (!ms) return '—';
  if (ms < 1000) return `${Math.round(ms)}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${Math.floor(ms / 60000)}m ${Math.round((ms % 60000) / 1000)}s`;
};

export const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });
};

export const truncate = (str, len = 50) =>
  str?.length > len ? str.slice(0, len) + '...' : str;

export const capitalize = (str) =>
  str?.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, ' ');
