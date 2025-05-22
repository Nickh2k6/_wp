/**
 * 深度合併兩個物件
 * @param {Object} obj1 - 目標物件
 * @param {Object} obj2 - 來源物件
 * @returns {Object} - 合併後的物件
 */
function deepMerge(obj1, obj2) {
    // 建立一個目標物件的複本，避免修改原始物件
    const result = { ...obj1 };
    
    // 遍歷來源物件的所有鍵值
    for (const key in obj2) {
      // 確保只處理物件自身的屬性，不包含繼承的屬性
      if (Object.prototype.hasOwnProperty.call(obj2, key)) {
        // 檢查來源物件和目標物件中的值是否都是物件（且不為 null）
        if (
          obj2[key] && typeof obj2[key] === 'object' && 
          obj1[key] && typeof obj1[key] === 'object' && 
          !(obj2[key] instanceof Array) && 
          !(obj1[key] instanceof Array)
        ) {
          // 如果兩者都是物件，則遞迴合併
          result[key] = deepMerge(obj1[key], obj2[key]);
        } else {
          // 否則直接覆蓋
          result[key] = obj2[key];
        }
      }
    }
    
    return result;
  }
  
  // 測試範例
  const obj1 = { a: 1, b: { x: 2, y: 3 } };
  const obj2 = { b: { y: 5, z: 6 }, c: 7 };
  console.log(deepMerge(obj1, obj2));
  /*
  {
    a: 1,
    b: { x: 2, y: 5, z: 6 },
    c: 7
  }
  */
 //https://claude.ai/public/artifacts/462e37e5-eb3f-42c2-a4e1-0d7349b16d72