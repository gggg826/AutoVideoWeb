/**
 * 浏览器指纹采集模块
 * 收集 Canvas、WebGL、字体等指纹信息
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
   * 获取 WebGL 指纹
   * @returns {string|null} WebGL 指纹哈希
   */
  getWebGLFingerprint() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

      if (!gl) return null;

      const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
      if (!debugInfo) return null;

      const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) || '';
      const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '';

      return this.hashCode(vendor + '|' + renderer);
    } catch (e) {
      console.warn('WebGL fingerprint failed:', e);
      return null;
    }
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
   * 收集所有指纹信息
   * @returns {Promise<Object>} 指纹数据对象
   */
  async collect() {
    return {
      canvas_fingerprint: this.getCanvasFingerprint(),
      webgl_fingerprint: this.getWebGLFingerprint(),
      fonts_hash: this.getFontsHash(),
      screen_resolution: `${screen.width}x${screen.height}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      language: navigator.language,
      platform: navigator.platform,
    };
  }
};
