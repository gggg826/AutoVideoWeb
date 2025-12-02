/**
 * AdAlliance 访问追踪器
 * 主追踪脚本 - 负责初始化追踪、记录行为数据
 */

(function() {
  'use strict';

  // 配置
  const API_BASE = window.location.origin + '/api/v1';
  const MOUSE_SAMPLE_INTERVAL = 200; // 鼠标移动采样间隔（毫秒）
  const MAX_MOUSE_SAMPLES = 50; // 最大鼠标轨迹采样数

  // 状态变量
  let visitId = null;
  let startTime = Date.now();
  let maxScrollDepth = 0;
  let mouseMoves = [];
  let isTracking = false;

  /**
   * 初始化追踪器
   */
  async function init() {
    if (isTracking) return;
    isTracking = true;

    try {
      console.log('🚀 AdAlliance Tracker 初始化中...');

      // 收集浏览器指纹
      const fingerprint = await FingerprintCollector.collect();

      // 发送初始追踪请求
      const response = await fetch(`${API_BASE}/track/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_agent: navigator.userAgent,
          referrer: document.referrer || null,
          page_url: window.location.href,
          ...fingerprint
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      visitId = data.visit_id;

      console.log('✅ 追踪初始化成功');
      console.log(`📊 Visit ID: ${visitId}`);
      console.log(`🎯 真实性评分: ${data.authenticity_score.toFixed(1)}`);
      console.log(`📱 设备类型: ${data.device_type || 'unknown'}`);

      // 设置事件监听器
      setupEventListeners();

    } catch (error) {
      console.error('❌ 追踪器初始化失败:', error);
      isTracking = false;
    }
  }

  /**
   * 设置事件监听器
   */
  function setupEventListeners() {
    // 监听滚动事件（节流）
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        calculateScrollDepth();
      }, 100);
    });

    // 监听鼠标移动事件（采样）
    let mouseTimeout;
    window.addEventListener('mousemove', (e) => {
      clearTimeout(mouseTimeout);
      mouseTimeout = setTimeout(() => {
        recordMouseMove(e.clientX, e.clientY);
      }, MOUSE_SAMPLE_INTERVAL);
    });

    // 页面卸载前发送行为数据
    window.addEventListener('beforeunload', sendBehaviorData);

    // 页面隐藏时发送行为数据
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        sendBehaviorData();
      }
    });

    // 定期发送行为数据（每 30 秒）
    setInterval(() => {
      sendBehaviorData(false); // 不是最终数据
    }, 30000);
  }

  /**
   * 计算滚动深度
   */
  function calculateScrollDepth() {
    const scrolled = window.scrollY || window.pageYOffset;
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;

    if (totalHeight > 0) {
      const depth = Math.round((scrolled / totalHeight) * 100);
      maxScrollDepth = Math.max(maxScrollDepth, Math.min(100, depth));
    }
  }

  /**
   * 记录鼠标移动
   * @param {number} x - X 坐标
   * @param {number} y - Y 坐标
   */
  function recordMouseMove(x, y) {
    const time = Date.now() - startTime;
    mouseMoves.push({ x, y, t: time });

    // 限制数组大小
    if (mouseMoves.length > MAX_MOUSE_SAMPLES) {
      mouseMoves = mouseMoves.slice(-MAX_MOUSE_SAMPLES);
    }
  }

  /**
   * 发送行为数据到服务器
   * @param {boolean} isFinal - 是否为最终数据
   */
  function sendBehaviorData(isFinal = true) {
    if (!visitId) return;

    const duration = Math.round((Date.now() - startTime) / 1000);

    const data = {
      visit_id: visitId,
      stay_duration: duration,
      scroll_depth: maxScrollDepth,
      mouse_movements: JSON.stringify(mouseMoves.slice(-20)) // 只发送最后 20 个采样
    };

    // 使用 sendBeacon 确保数据发送（即使页面卸载）
    if (isFinal && navigator.sendBeacon) {
      const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
      navigator.sendBeacon(`${API_BASE}/track/behavior`, blob);
    } else {
      // 使用 fetch（异步，不阻塞）
      fetch(`${API_BASE}/track/behavior`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        keepalive: true // 即使页面卸载也继续请求
      }).catch(err => {
        console.warn('行为数据发送失败:', err);
      });
    }

    if (isFinal) {
      console.log('📤 最终行为数据已发送');
      console.log(`⏱️  停留时间: ${duration}秒`);
      console.log(`📜 滚动深度: ${maxScrollDepth}%`);
      console.log(`🖱️  鼠标移动: ${mouseMoves.length} 次采样`);
    }
  }

  /**
   * 页面加载完成后初始化
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露 API（用于调试）
  window.AdAllianceTracker = {
    getVisitId: () => visitId,
    getStats: () => ({
      visitId,
      duration: Math.round((Date.now() - startTime) / 1000),
      scrollDepth: maxScrollDepth,
      mouseSamples: mouseMoves.length
    }),
    sendData: () => sendBehaviorData(false)
  };

})();
