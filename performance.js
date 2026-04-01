/**
 * 性能监控模块
 * @namespace Performance
 */
const Performance = {
  /**
   * 性能指标存储
   * @private
   */
  _metrics: {
    filter: { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 },
    render: { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 },
    analysis: { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 },
    storage: { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 }
  },

  /**
   * 开始性能计时
   * @param {string} key - 指标名称
   * @returns {number} 开始时间戳
   */
  start: (key) => {
    if(!Performance._metrics[key]) {
      Performance._metrics[key] = { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 };
    }
    return performance.now();
  },

  /**
   * 结束性能计时并记录
   * @param {string} key - 指标名称
   * @param {number} startTime - 开始时间戳
   */
  end: (key, startTime) => {
    if(!Performance._metrics[key]) return;
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    const metric = Performance._metrics[key];
    metric.count++;
    metric.totalTime += duration;
    metric.min = Math.min(metric.min, duration);
    metric.max = Math.max(metric.max, duration);
    metric.avg = metric.totalTime / metric.count;
  },

  /**
   * 获取性能指标
   * @param {string} key - 指标名称
   * @returns {Object} 性能指标
   */
  getMetric: (key) => {
    return Performance._metrics[key] || null;
  },

  /**
   * 获取所有性能指标
   * @returns {Object} 所有性能指标
   */
  getAllMetrics: () => {
    return { ...Performance._metrics };
  },

  /**
   * 重置性能指标
   * @param {string} key - 指标名称
   */
  reset: (key) => {
    if(key) {
      Performance._metrics[key] = { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 };
    } else {
      Object.keys(Performance._metrics).forEach(k => {
        Performance._metrics[k] = { count: 0, totalTime: 0, min: Infinity, max: 0, avg: 0 };
      });
    }
  },

  /**
   * 打印性能报告
   */
  printReport: () => {
    console.log('=== 性能监控报告 ===');
    Object.entries(Performance._metrics).forEach(([key, metric]) => {
      if(metric.count > 0) {
        console.log(`${key}:`);
        console.log(`  调用次数: ${metric.count}`);
        console.log(`  总时间: ${metric.totalTime.toFixed(2)}ms`);
        console.log(`  平均时间: ${metric.avg.toFixed(2)}ms`);
        console.log(`  最小时间: ${metric.min.toFixed(2)}ms`);
        console.log(`  最大时间: ${metric.max.toFixed(2)}ms`);
      }
    });
  }
};

// 导出模块
if(typeof window !== 'undefined') {
  window.Performance = Performance;
}
