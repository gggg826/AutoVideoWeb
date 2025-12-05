/**
 * 管理后台 API 调用封装
 */

const API_BASE = window.location.origin + '/api/v1';

/**
 * Get authorization headers
 */
function getAuthHeaders() {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    // Redirect to login if no token
    window.location.href = '/admin/login.html';
    throw new Error('No authentication token');
  }

  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
}

/**
 * Handle authentication errors
 */
function handleAuthError(response) {
  if (response.status === 401 || response.status === 403) {
    // Clear token and redirect to login
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_token_expires');
    window.location.href = '/admin/login.html';
  }
}

const API = {
  /**
   * 通用 GET 请求
   */
  async get(endpoint, params = {}) {
    const url = new URL(`${API_BASE}${endpoint}`);
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        url.searchParams.append(key, params[key]);
      }
    });

    const response = await fetch(url, {
      headers: getAuthHeaders()
    });

    handleAuthError(response);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  /**
   * 通用 POST 请求
   */
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });

    handleAuthError(response);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  /**
   * 通用 DELETE 请求
   */
  async delete(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });

    handleAuthError(response);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  // 统计相关 API
  stats: {
    async getSummary(days = 7) {
      return await API.get('/admin/stats/summary', { days });
    },

    async getTrend(days = 7) {
      return await API.get('/admin/stats/trend', { days });
    },

    async getDevices(days = 7) {
      return await API.get('/admin/stats/devices', { days });
    },

    async getLocations(days = 7) {
      return await API.get('/admin/stats/locations', { days });
    },

    async getReferrers(days = 7) {
      return await API.get('/admin/stats/referrers', { days });
    }
  },

  // 访问记录相关 API
  visits: {
    async getList(params = {}) {
      return await API.get('/admin/visits', params);
    },

    async getDetail(visitId) {
      return await API.get(`/admin/visits/${visitId}`);
    },

    async delete(visitId) {
      return await API.delete(`/admin/visits/${visitId}`);
    }
  }
};

/**
 * 数据格式化工具
 */
const Format = {
  /**
   * 格式化日期时间
   */
  datetime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  },

  /**
   * 格式化日期
   */
  date(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
  },

  /**
   * 格式化时长（秒）
   */
  duration(seconds) {
    if (!seconds || seconds === 0) return '0秒';

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    const parts = [];
    if (hours > 0) parts.push(`${hours}小时`);
    if (minutes > 0) parts.push(`${minutes}分钟`);
    if (secs > 0 || parts.length === 0) parts.push(`${secs}秒`);

    return parts.join('');
  },

  /**
   * 格式化评分
   */
  score(score) {
    if (!score && score !== 0) return '-';
    return score.toFixed(1);
  },

  /**
   * 格式化百分比
   */
  percent(value) {
    if (!value && value !== 0) return '0%';
    return value.toFixed(1) + '%';
  },

  /**
   * 格式化设备类型
   */
  deviceType(type) {
    const types = {
      'pc': '💻 电脑',
      'mobile': '📱 手机',
      'tablet': '📱 平板',
      'bot': '🤖 机器人'
    };
    return types[type] || type || '-';
  },

  /**
   * 格式化布尔值
   */
  boolean(value) {
    return value ? '✅ 是' : '❌ 否';
  },

  /**
   * 格式化徽章
   */
  badge(score) {
    if (score >= 80) {
      return '<span class="badge badge-success">优秀</span>';
    } else if (score >= 60) {
      return '<span class="badge badge-info">良好</span>';
    } else if (score >= 40) {
      return '<span class="badge badge-warning">一般</span>';
    } else {
      return '<span class="badge badge-danger">较差</span>';
    }
  }
};

/**
 * 通用工具函数
 */
const Utils = {
  /**
   * 显示加载状态
   */
  showLoading(element) {
    element.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  },

  /**
   * 显示错误消息
   */
  showError(element, message) {
    element.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">⚠️</div>
        <p>${message}</p>
      </div>
    `;
  },

  /**
   * 显示空状态
   */
  showEmpty(element, message = '暂无数据') {
    element.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📭</div>
        <p>${message}</p>
      </div>
    `;
  },

  /**
   * 防抖函数
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  /**
   * 复制到剪贴板
   */
  async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      alert('已复制到剪贴板');
    } catch (err) {
      console.error('复制失败:', err);
      alert('复制失败');
    }
  },

  /**
   * 导出为 CSV
   */
  exportToCSV(data, filename) {
    const csv = this.convertToCSV(data);
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  },

  /**
   * 转换为 CSV 格式
   */
  convertToCSV(data) {
    if (!data || data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const rows = data.map(obj =>
      headers.map(header => {
        const value = obj[header];
        // 转义包含逗号或引号的值
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      }).join(',')
    );

    return [headers.join(','), ...rows].join('\n');
  }
};
