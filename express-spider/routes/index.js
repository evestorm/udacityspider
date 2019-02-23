var express = require('express');
var router = express.Router();
var db = require("../config/db");

const fs = require('fs');

// "结巴"中文分词的Node.js版本 https: //github.com/yanyiwu/nodejieba

// 使用参考：
// 1. https://blog.csdn.net/zhang6223284/article/details/81263986
// 2. https: //blog.csdn.net/qq_38950721/article/details/72781600
const nodejieba = require('nodejieba');
// 载入自己的用户词典
nodejieba.load({
  userDict: 'public/dict/userdict.utf8'
})

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/searchKeyWords', function (req, res, next) {
  res.header("Content-Type", "application/json; charset=utf-8")
  db.row(`SELECT searchKeyWords FROM job_list GROUP BY searchKeyWords`).then(data => {
    let citySet = new Set(data.map(item => item.city))
    let cityArr = Array.from(citySet).map(item => {
      return {
        name: item,
        value: [0, 0, 0]
      }
    })
    for (let i = 0; i < data.length; i++) {
      let {
        city,
        longitude,
        latitude
      } = data[i]
      for (const cityObj of cityArr) {
        if (cityObj.name == city) {
          if (cityObj.value[0] == 0) {
            cityObj.value[0] = longitude
          }
          if (cityObj.value[1] == 0) {
            cityObj.value[1] = latitude
          }
          cityObj.value[2] += 1
        }
      }
    }
    res.json({
      msg: "操作成功",
      status: 200,
      datas: cityArr
    });
  }, err => {
    res.json({
      msg: "数据为空",
      status: 500,
      datas: [],
      err: err
    });
  })
})

// 获取某个职位下的城市分布信息
router.get('/cityInfo', function (req, res, next) {
  res.header("Content-Type", "application/json; charset=utf-8")

  let param = req.query || req.params
  console.log(req.query, req.params)
  let {
    searchWords
  } = param

  if (!searchWords) {
    res.end(JSON.stringify({
      msg: '请选择某一职位的关键词',
      status: '102'
    }));
    return;
  }

  db.row(`SELECT city, longitude, latitude FROM job_list WHERE searchKeyWords = '${searchWords}'`).then(data => {
    let citySet = new Set(data.map(item => item.city))
    let cityArr = Array.from(citySet).map(item => {
      return {
        name: item,
        value: [0, 0, 0]
      }
    })
    for (let i = 0; i < data.length; i++) {
      let {
        city,
        longitude,
        latitude
      } = data[i]
      for (const cityObj of cityArr) {
        if (cityObj.name == city) {
          if (cityObj.value[0] == 0) {
            cityObj.value[0] = longitude
          }
          if (cityObj.value[1] == 0) {
            cityObj.value[1] = latitude
          }
          cityObj.value[2] += 1
        }
      }
    }
    res.json({
      msg: "操作成功",
      status: 200,
      datas: cityArr
    });
  }, err => {
    res.json({
      msg: "数据为空",
      status: 500,
      datas: [],
      err: err
    });
  })
})

router.get('/jieba', function (req, res, next) {
  res.header("Content-Type", "application/json; charset=utf-8")

  let param = req.query || req.params
  console.log(req.query, req.params)
  let { searchWords } = param

  if (!searchWords) {
    res.end(JSON.stringify({
      msg: '请选择某一职位的关键词',
      status: '102'
    }));
    return;
  }

  db.row(`SELECT job_detail.description FROM 
      job_list INNER JOIN 
      job_detail ON job_list.positionId = job_detail.positionId 
      WHERE job_list.searchKeyWords = '${searchWords}'`).then(data => {
    // 通过循环来汇总描述
    let sentence = ''
    for (const desc of data) {
      sentence += desc.description
    }
    // 取权重前500的词
    let result = nodejieba.extract(sentence, 100)
    // 从TOP500中找出符合tagList的结果
    // let tagList = ['HTML', '框架', 'JavaScript', 'CSS', '布局', 'H5', '混合开发', 'jquery', 'bootstrap', 'vue', 'angular', 'react', 'ajax', '响应式', 'CSS3', 'ES6', 'REST', 'node', 'zepto', 'mvc', 'mvvm', 'Babel', 'npm', 'webpack', 'gulp', "git", 'sass', 'scss', '优化', '动画', 'native', 'hybrid', 'python']
    let tagList = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '团队', '熟练掌握', '开发', '能力', '熟悉', '经验', '优先', '要求', '语言', '熟练', '参与', '任职', '相关', '良好', '负责', '具有', '文档', 'ing', 'My', '公司', '能够', '用户', '沟通', '领域', '数量掌握', '编程', '扎实', '了解', '推荐', '学习', '以上学历', '精通', '支持', '工作', '落地', '岗位', '岗位职责', '问题', '常用', '活动', '善于', '至少', '商汤']
    let filterResult = result.filter(item => tagList.indexOf(item.word) < 0)
    // let filterResult = result
    res.json({
      msg: "操作成功",
      status: 200,
      datas: filterResult
    });
  }, err => {
    res.json({
      msg: "数据为空",
      status: 500,
      datas: [],
      err: err
    });
  })
})

router.get('/otherinfo', async function (req, res, next) {
  res.header("Content-Type", "application/json; charset=utf-8")

  let param = req.query || req.params
  console.log(req.query, req.params)
  let {
    searchWords
  } = param

  if (!searchWords) {
    res.end(JSON.stringify({
      msg: '请选择某一职位的关键词',
      status: '102'
    }));
    return;
  }

  // 1. 先查询出每个职位的平均薪资
  // 2. 然后根据自定义范围计数
  let salary = await db.row(`
    SELECT
      (CASE WHEN avgNum <= 6 THEN '6k及以下'
        WHEN avgNum > 6 AND avgNum <= 8 THEN '6k-8k'
        WHEN avgNum > 8 AND avgNum <= 10 THEN '8k-10k'
        WHEN avgNum > 10 AND avgNum <= 15 THEN '10k-15k'
        WHEN avgNum > 15 AND avgNum <= 20 THEN '15k-20k'
        WHEN avgNum > 20 AND avgNum <= 35 THEN '20k-35k'
        ELSE '35k以上'
        END) AS 'name',
      COUNT(avgNum) AS 'value'
    FROM(
      SELECT floor(((REPLACE(SUBSTRING_INDEX(salary, '-', 1), 'k', '') +
        REPLACE(SUBSTRING_INDEX(
          SUBSTRING_INDEX(salary, '-', -1),
          '-',
          1
        ), 'k', '')) / 2)) AS avgNum FROM job_list WHERE searchKeyWords = '${searchWords}'
      ORDER BY avgNum) AS avgTable
    GROUP BY name
  `)

  let education = await db.row(`
    SELECT education AS 'name', COUNT(education) AS 'value'
    FROM job_list
    WHERE searchKeyWords = '${searchWords}'
    GROUP BY education
  `)


  db.row(`SELECT workYear AS 'name', COUNT(workYear) AS 'value' FROM
      job_list WHERE searchKeyWords = '${searchWords}'
      GROUP BY workYear`).then(data => {
    
    // let filterResult = result
    res.json({
      msg: "操作成功",
      status: 200,
      datas: {
        "work": data,
        "salary": salary || [],
        "education": education
      }
    });
  }, err => {
    res.json({
      msg: "数据为空",
      status: 500,
      datas: [],
      err: err
    });
  })
})

module.exports = router;
