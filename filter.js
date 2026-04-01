/**
 * 筛选逻辑管理器
 * @namespace Filter
 */
const Filter = {
  /**
   * 通用筛选函数
   * @param {Object|null} selected - 选中的筛选条件
   * @param {Array|null} excluded - 排除的号码
   * @returns {Array} 筛选后的号码列表
   */
  getFilteredList: (selected = null, excluded = null) => {
    const startTime = typeof Performance !== 'undefined' ? Performance.start('filter') : 0;
    
    try {
      const state = StateManager._state;
      const targetSelected = selected || state.selected;
      const targetExcluded = excluded || state.excluded;
      const numList = state.numList;

      // 优化：提前计算需要检查的分组
      const activeGroups = [];
      for(const group in targetSelected){
        if(targetSelected[group].length > 0) {
          activeGroups.push({ group, values: targetSelected[group] });
        }
      }

      // 优化：使用Set进行快速查找
      const excludedSet = new Set(targetExcluded);

      const result = numList.filter(item => {
        if(excludedSet.has(item.num)) return false;
        
        // 只检查有选择的分组
        for(const { group, values } of activeGroups){
          if(!values.includes(item[group])) return false;
        }
        return true;
      });
      
      if(typeof Performance !== 'undefined') {
        Performance.end('filter', startTime);
      }
      
      return result;
    } catch(e) {
      console.error('筛选失败', e);
      if(typeof Performance !== 'undefined') {
        Performance.end('filter', startTime);
      }
      return [];
    }
  },

  /**
   * 全选所有筛选条件（防抖优化）
   */
  selectAllFilters: Utils.debounce(() => {
    const state = StateManager._state;
    Object.keys(state.selected).forEach(group => StateManager.selectGroup(group));
    Toast.show('已全选所有筛选条件');
  }, CONFIG.CLICK_DEBOUNCE_DELAY),

  /**
   * 清除所有筛选条件（防抖优化）
   */
  clearAllFilters: Utils.debounce(() => {
    const state = StateManager._state;
    // 重置所有筛选条件
    Object.keys(state.selected).forEach(group => StateManager.resetGroup(group));
    // 重置排除号码
    StateManager.setState({
      excluded: [],
      excludeHistory: [],
      lockExclude: false
    });
    // 更新复选框
    DOM.lockExclude.checked = false;
    Toast.show('已清除所有筛选与排除条件');
  }, CONFIG.CLICK_DEBOUNCE_DELAY)
};
