/**
 * 浏览器指纹采集模块
 * 收集 Canvas、WebGL、字体、硬件、网络等指纹信息
 */

const FingerprintCollector = {
  /**
   * 获取 Canvas 指纹
   * @returns {string|null} Canvas 指纹哈希
   */
  getCanvasFingerprint() {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 200;
      canvas.height = 50;

      // 绘制文本
      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillStyle = '#f60';
      ctx.fillRect(0, 0, 100, 50);
      ctx.fillStyle = '#069';
      ctx.fillText('AdAlliance 🎨', 2, 15);

      // 生成指纹
      return this.hashCode(canvas.toDataURL());
    } catch (e) {
      console.warn('Canvas fingerprint failed:', e);
      return null;
    }
  },

  /**
   * 获取 WebGL 指纹和详细信息
   * @returns {Object} WebGL 指纹数据
   */
  getWebGLInfo() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

      if (!gl) return { fingerprint: null, vendor: null, renderer: null };

      const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
      let vendor = null;
      let renderer = null;

      if (debugInfo) {
        vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) || null;
        renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || null;
      }

      const fingerprint = vendor && renderer ? this.hashCode(vendor + '|' + renderer) : null;

      return { fingerprint, vendor, renderer };
    } catch (e) {
      console.warn('WebGL fingerprint failed:', e);
      return { fingerprint: null, vendor: null, renderer: null };
    }
  },

  /**
   * 获取 WebGL 指纹（兼容旧接口）
   * @returns {string|null} WebGL 指纹哈希
   */
  getWebGLFingerprint() {
    return this.getWebGLInfo().fingerprint;
  },

  /**
   * 检测可用字体并生成哈希
   * @returns {string|null} 字体列表哈希
   */
  getFontsHash() {
    const baseFonts = ['monospace', 'sans-serif', 'serif'];
    const testFonts = [
      'Arial', 'Verdana', 'Times New Roman', 'Courier New',
      'Georgia', 'Palatino', 'Garamond', 'Comic Sans MS',
      'Trebuchet MS', 'Arial Black', 'Impact', 'Tahoma',
      'Helvetica', 'Calibri', 'Consolas', 'Monaco'
    ];

    const detectedFonts = [];

    for (const font of testFonts) {
      if (this.isFontAvailable(font, baseFonts)) {
        detectedFonts.push(font);
      }
    }

    return this.hashCode(detectedFonts.join(','));
  },

  /**
   * 检查字体是否可用
   * @param {string} fontName - 字体名称
   * @param {Array} baseFonts - 基础字体列表
   * @returns {boolean} 字体是否可用
   */
  isFontAvailable(fontName, baseFonts) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const text = 'mmmmmmmmmmlli';

    // 使用基础字体测量宽度
    ctx.font = `72px ${baseFonts[0]}`;
    const baseWidth = ctx.measureText(text).width;

    // 使用目标字体测量宽度
    ctx.font = `72px "${fontName}", ${baseFonts[0]}`;
    const testWidth = ctx.measureText(text).width;

    // 如果宽度不同，说明字体可用
    return baseWidth !== testWidth;
  },

  /**
   * 简单哈希函数
   * @param {string} str - 输入字符串
   * @returns {string} 十六进制哈希值
   */
  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为 32 位整数
    }
    return Math.abs(hash).toString(16);
  },

  /**
   * 获取浏览器地理位置（需要用户授权）
   * @returns {Promise<Object|null>} 地理位置数据或 null
   */
  async getGeolocation() {
    return new Promise((resolve) => {
      // 检查浏览器是否支持地理位置API
      if (!navigator.geolocation) {
        console.log('浏览器不支持地理位置API');
        resolve(null);
        return;
      }

      // 请求地理位置（不阻塞页面加载）
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // 成功获取位置
          const coords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            altitude: position.coords.altitude,
            altitude_accuracy: position.coords.altitudeAccuracy
          };
          console.log('✅ 获取到浏览器地理位置:', coords);
          resolve(coords);
        },
        (error) => {
          // 用户拒绝或其他错误
          let errorMsg = '未知错误';
          switch(error.code) {
            case error.PERMISSION_DENIED:
              errorMsg = '用户拒绝地理位置授权';
              break;
            case error.POSITION_UNAVAILABLE:
              errorMsg = '位置信息不可用';
              break;
            case error.TIMEOUT:
              errorMsg = '获取位置超时';
              break;
          }
          console.log(`⚠️ 地理位置获取失败: ${errorMsg}`);
          resolve(null);
        },
        {
          timeout: 8000,           // 8秒超时
          maximumAge: 300000,      // 接受5分钟内的缓存位置
          enableHighAccuracy: false // 不启用高精度（避免过长等待）
        }
      );
    });
  },

  /**
   * 获取硬件信息
   * @returns {Object} 硬件信息
   */
  getHardwareInfo() {
    return {
      // 设备内存（GB，某些浏览器可能返回近似值或不支持）
      device_memory: navigator.deviceMemory || null,
      // CPU 核心数
      hardware_concurrency: navigator.hardwareConcurrency || null,
      // 颜色深度
      color_depth: screen.colorDepth || null,
      // 设备像素比
      pixel_ratio: window.devicePixelRatio || null,
      // 最大触点数（用于判断是否触屏设备）
      max_touch_points: navigator.maxTouchPoints || 0
    };
  },

  /**
   * 获取网络信息
   * @returns {Object} 网络信息
   */
  getNetworkInfo() {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;

    if (!connection) {
      return {
        connection_type: null,
        connection_downlink: null,
        connection_rtt: null,
        connection_save_data: null
      };
    }

    return {
      // 网络类型 (slow-2g, 2g, 3g, 4g)
      connection_type: connection.effectiveType || null,
      // 下行速度 (Mbps)
      connection_downlink: connection.downlink || null,
      // 网络延迟 (ms)
      connection_rtt: connection.rtt || null,
      // 是否开启省流量模式
      connection_save_data: connection.saveData || false
    };
  },

  /**
   * 获取浏览器功能检测
   * @returns {Object} 浏览器功能
   */
  getBrowserFeatures() {
    return {
      // Cookie 是否启用
      cookies_enabled: navigator.cookieEnabled || false,
      // Do Not Track 状态
      do_not_track: navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.msDoNotTrack === '1',
      // PDF 查看器是否启用
      pdf_viewer_enabled: navigator.pdfViewerEnabled !== undefined ? navigator.pdfViewerEnabled : null
    };
  },

  /**
   * 获取插件列表哈希
   * @returns {string|null} 插件哈希
   */
  getPluginsHash() {
    try {
      const plugins = navigator.plugins;
      if (!plugins || plugins.length === 0) return null;

      const pluginList = [];
      for (let i = 0; i < plugins.length; i++) {
        pluginList.push(plugins[i].name + '|' + plugins[i].filename);
      }
      return this.hashCode(pluginList.join(','));
    } catch (e) {
      console.warn('Plugins hash failed:', e);
      return null;
    }
  },

  /**
   * 获取音频指纹
   * @returns {Promise<string|null>} 音频指纹哈希
   */
  async getAudioFingerprint() {
    return new Promise((resolve) => {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) {
          resolve(null);
          return;
        }

        const audioContext = new AudioContext();
        const oscillator = audioContext.createOscillator();
        const analyser = audioContext.createAnalyser();
        const gainNode = audioContext.createGain();
        const scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

        // 设置参数
        oscillator.type = 'triangle';
        oscillator.frequency.value = 10000;
        gainNode.gain.value = 0; // 静音

        // 连接节点
        oscillator.connect(analyser);
        analyser.connect(scriptProcessor);
        scriptProcessor.connect(gainNode);
        gainNode.connect(audioContext.destination);

        let fingerprint = null;

        scriptProcessor.onaudioprocess = (e) => {
          const output = e.inputBuffer.getChannelData(0);
          let sum = 0;
          for (let i = 0; i < output.length; i++) {
            sum += Math.abs(output[i]);
          }
          fingerprint = sum.toString();

          // 清理资源
          oscillator.disconnect();
          analyser.disconnect();
          scriptProcessor.disconnect();
          gainNode.disconnect();

          if (audioContext.state !== 'closed') {
            audioContext.close();
          }

          resolve(fingerprint ? this.hashCode(fingerprint) : null);
        };

        oscillator.start(0);

        // 超时处理
        setTimeout(() => {
          if (!fingerprint) {
            oscillator.disconnect();
            analyser.disconnect();
            scriptProcessor.disconnect();
            gainNode.disconnect();
            if (audioContext.state !== 'closed') {
              audioContext.close();
            }
            resolve(null);
          }
        }, 1000);

      } catch (e) {
        console.warn('Audio fingerprint failed:', e);
        resolve(null);
      }
    });
  },

  /**
   * 获取媒体设备哈希
   * @returns {Promise<string|null>} 媒体设备哈希
   */
  async getMediaDevicesHash() {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
        return null;
      }

      const devices = await navigator.mediaDevices.enumerateDevices();

      // 统计设备类型数量（不获取具体ID以保护隐私）
      const deviceCounts = {
        audioinput: 0,
        audiooutput: 0,
        videoinput: 0
      };

      devices.forEach(device => {
        if (deviceCounts[device.kind] !== undefined) {
          deviceCounts[device.kind]++;
        }
      });

      const deviceString = `audio_in:${deviceCounts.audioinput}|audio_out:${deviceCounts.audiooutput}|video_in:${deviceCounts.videoinput}`;
      return this.hashCode(deviceString);
    } catch (e) {
      console.warn('Media devices hash failed:', e);
      return null;
    }
  },

  /**
   * 获取存储支持检测
   * @returns {Object} 存储支持状态
   */
  getStorageSupport() {
    return {
      // localStorage 是否可用
      local_storage_enabled: this.isStorageAvailable('localStorage'),
      // sessionStorage 是否可用
      session_storage_enabled: this.isStorageAvailable('sessionStorage'),
      // IndexedDB 是否可用
      indexed_db_enabled: !!window.indexedDB
    };
  },

  /**
   * 检测存储是否可用
   * @param {string} type - 存储类型
   * @returns {boolean} 是否可用
   */
  isStorageAvailable(type) {
    try {
      const storage = window[type];
      const testKey = '__storage_test__';
      storage.setItem(testKey, testKey);
      storage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  },

  /**
   * 检测广告拦截器
   * @returns {Promise<boolean>} 是否检测到广告拦截器
   */
  async detectAdBlocker() {
    return new Promise((resolve) => {
      try {
        // 创建一个模拟广告的元素
        const adElement = document.createElement('div');
        adElement.innerHTML = '&nbsp;';
        adElement.className = 'adsbox ad-banner ad-container';
        adElement.style.cssText = 'position:absolute;top:-1000px;left:-1000px;width:1px;height:1px;';
        document.body.appendChild(adElement);

        // 检测元素是否被隐藏
        setTimeout(() => {
          const isBlocked = adElement.offsetParent === null ||
                           adElement.offsetHeight === 0 ||
                           adElement.offsetWidth === 0 ||
                           window.getComputedStyle(adElement).display === 'none';

          document.body.removeChild(adElement);
          resolve(isBlocked);
        }, 100);
      } catch (e) {
        console.warn('Ad blocker detection failed:', e);
        resolve(false);
      }
    });
  },

  /**
   * 获取 Battery 信息（如果可用）
   * @returns {Promise<Object|null>} 电池信息
   */
  async getBatteryInfo() {
    try {
      if (!navigator.getBattery) {
        return null;
      }

      const battery = await navigator.getBattery();
      return {
        battery_charging: battery.charging,
        battery_level: Math.round(battery.level * 100),
        battery_charging_time: battery.chargingTime === Infinity ? null : battery.chargingTime,
        battery_discharging_time: battery.dischargingTime === Infinity ? null : battery.dischargingTime
      };
    } catch (e) {
      console.warn('Battery info failed:', e);
      return null;
    }
  },

  /**
   * 获取 WebRTC 本地 IP（用于指纹，不是实际IP）
   * @returns {Promise<string|null>} WebRTC 哈希
   */
  async getWebRTCHash() {
    return new Promise((resolve) => {
      try {
        const RTCPeerConnection = window.RTCPeerConnection ||
                                   window.mozRTCPeerConnection ||
                                   window.webkitRTCPeerConnection;

        if (!RTCPeerConnection) {
          resolve(null);
          return;
        }

        const pc = new RTCPeerConnection({
          iceServers: []
        });

        pc.createDataChannel('');

        const candidates = [];

        pc.onicecandidate = (e) => {
          if (!e.candidate) {
            pc.close();
            if (candidates.length > 0) {
              resolve(this.hashCode(candidates.join('|')));
            } else {
              resolve(null);
            }
            return;
          }
          candidates.push(e.candidate.candidate);
        };

        pc.createOffer()
          .then(offer => pc.setLocalDescription(offer))
          .catch(() => {
            pc.close();
            resolve(null);
          });

        // 超时处理
        setTimeout(() => {
          if (candidates.length === 0) {
            pc.close();
            resolve(null);
          }
        }, 3000);

      } catch (e) {
        console.warn('WebRTC hash failed:', e);
        resolve(null);
      }
    });
  },

  /**
   * 获取 Speech Voices 哈希
   * @returns {Promise<string|null>} 语音列表哈希
   */
  async getSpeechVoicesHash() {
    return new Promise((resolve) => {
      try {
        if (!window.speechSynthesis) {
          resolve(null);
          return;
        }

        const getVoices = () => {
          const voices = window.speechSynthesis.getVoices();
          if (voices.length > 0) {
            const voiceNames = voices.map(v => v.name + '|' + v.lang).join(',');
            resolve(this.hashCode(voiceNames));
          } else {
            resolve(null);
          }
        };

        // 某些浏览器需要异步加载
        if (window.speechSynthesis.getVoices().length > 0) {
          getVoices();
        } else {
          window.speechSynthesis.onvoiceschanged = getVoices;
          // 超时处理
          setTimeout(() => resolve(null), 1000);
        }
      } catch (e) {
        console.warn('Speech voices hash failed:', e);
        resolve(null);
      }
    });
  },

  /**
   * 获取 Performance 指标
   * @returns {Object} 性能指标
   */
  getPerformanceMetrics() {
    try {
      if (!window.performance || !window.performance.timing) {
        return null;
      }

      const timing = window.performance.timing;
      return {
        // 页面加载时间
        page_load_time: timing.loadEventEnd - timing.navigationStart,
        // DOM 解析时间
        dom_parse_time: timing.domContentLoadedEventEnd - timing.navigationStart,
        // DNS 查询时间
        dns_time: timing.domainLookupEnd - timing.domainLookupStart,
        // TCP 连接时间
        tcp_time: timing.connectEnd - timing.connectStart,
        // 首字节时间
        ttfb: timing.responseStart - timing.navigationStart
      };
    } catch (e) {
      console.warn('Performance metrics failed:', e);
      return null;
    }
  },

  /**
   * 检测是否为 Headless 浏览器
   * @returns {boolean} 是否可能是 Headless
   */
  detectHeadless() {
    try {
      // 检测各种 Headless 特征
      const checks = {
        // 检测 WebDriver
        webdriver: navigator.webdriver === true,
        // 检测 Chrome Headless
        chromeHeadless: /HeadlessChrome/.test(navigator.userAgent),
        // 检测 Phantom
        phantom: !!window._phantom || !!window.callPhantom,
        // 检测 Nightmare
        nightmare: !!window.__nightmare,
        // 检测 Selenium
        selenium: !!window.document.__selenium_unwrapped || !!window.document.__webdriver_evaluate,
        // 检测 Puppeteer
        puppeteer: !!window.__puppeteer_evaluation_script__,
        // 检测 Chrome 自动化
        chromeAuto: !!window.chrome && !window.chrome.runtime,
        // 检测缺少 plugins
        noPlugins: navigator.plugins.length === 0,
        // 检测缺少语言
        noLanguages: !navigator.languages || navigator.languages.length === 0
      };

      return Object.values(checks).some(v => v === true);
    } catch (e) {
      return false;
    }
  },

  /**
   * 收集所有指纹信息
   * @returns {Promise<Object>} 指纹数据对象
   */
  async collect() {
    // 获取 WebGL 详细信息
    const webglInfo = this.getWebGLInfo();

    // 获取硬件信息
    const hardwareInfo = this.getHardwareInfo();

    // 获取网络信息
    const networkInfo = this.getNetworkInfo();

    // 获取浏览器功能
    const browserFeatures = this.getBrowserFeatures();

    // 获取存储支持
    const storageSupport = this.getStorageSupport();

    // 并行获取异步指纹
    const [
      geolocation,
      audioFingerprint,
      mediaDevicesHash,
      adBlockerDetected,
      batteryInfo,
      webrtcHash,
      speechVoicesHash
    ] = await Promise.all([
      this.getGeolocation(),
      this.getAudioFingerprint(),
      this.getMediaDevicesHash(),
      this.detectAdBlocker(),
      this.getBatteryInfo(),
      this.getWebRTCHash(),
      this.getSpeechVoicesHash()
    ]);

    // 获取性能指标
    const performanceMetrics = this.getPerformanceMetrics();

    // 检测 Headless
    const isHeadless = this.detectHeadless();

    return {
      // 基础指纹
      canvas_fingerprint: this.getCanvasFingerprint(),
      webgl_fingerprint: webglInfo.fingerprint,
      fonts_hash: this.getFontsHash(),
      screen_resolution: `${screen.width}x${screen.height}`,
      viewport_size: `${window.innerWidth}x${window.innerHeight}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      language: navigator.language,
      platform: navigator.platform,

      // WebGL 详细信息
      webgl_vendor: webglInfo.vendor,
      webgl_renderer: webglInfo.renderer,

      // 硬件信息
      ...hardwareInfo,

      // 网络信息
      ...networkInfo,

      // 浏览器功能
      ...browserFeatures,
      plugins_hash: this.getPluginsHash(),

      // 音频指纹
      audio_fingerprint: audioFingerprint,

      // 媒体设备
      media_devices_hash: mediaDevicesHash,

      // 存储支持
      ...storageSupport,

      // 广告拦截检测
      ad_blocker_detected: adBlockerDetected,

      // 电池信息
      ...batteryInfo,

      // WebRTC 哈希
      webrtc_hash: webrtcHash,

      // 语音列表哈希
      speech_voices_hash: speechVoicesHash,

      // 性能指标
      performance_metrics: performanceMetrics,

      // Headless 检测
      is_headless: isHeadless,

      // 浏览器地理位置（可能为 null）
      geolocation: geolocation
    };
  }
};
