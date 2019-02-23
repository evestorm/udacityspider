var express = require('express');
var router = express.Router();
var db = require("../config/db");
const excelManger = require('../config/excelConfig')

// 查询列表页
router.get('/list', async function (req, res, next) {
    res.header("Content-Type", "application/json; charset=utf-8")

    let param = ''
    if (req.method == "POST") {
        param = req.body
    } else {
        param = req.query || req.params
    }
    console.log(req.query, req.params)
    let { page, cid, pname, stime, etime } = param
    
    if (!stime || !etime) {
        stime = ''
        etime = ''
    }

    if (!param.page || !param.cid) {
        res.end(JSON.stringify({
            msg: '请传入参数请求页面page以及职位分类cid',
            status: '102'
        }));
        return;
    }

    var start = (page - 1) * 20

    let where = ''
    let plistItem = await db.first('SELECT * FROM position_list WHERE id = ?', [param.cid])
    let searchKeyWords = plistItem["name"]
    where += 
        searchKeyWords !== '' ? 
        ` WHERE searchKeyWords = '${searchKeyWords}'` : ''
    where += pname && pname !== '' ? 
        ` AND positionName LIKE '%${pname}%'` : ''
    where += stime !== '' && etime !== '' ? 
        ` AND createTime BETWEEN '${stime}' AND '${etime}'` : ''
    console.log(where);

    // 提供前端表格展示的数据
    var sql = `
        SELECT COUNT(*) FROM job_list ${where};
        SELECT
            positionId,
            positionName,
            city,
            workYear,
            education,
            salary,
            companyShortName,
            jobNature,
            createTime,

            companySize,
            industryField,
            positionAdvantage,
            financeStage,
            positionLables,
            companyLabelList,
            companyFullName,
            isSchoolJob,
            skillLables
        FROM job_list ${where} limit ${start}, 20
    `

    db.row(sql).then(data => {
        // 所查询数据的总条数
        var allCount = data[0][0]['COUNT(*)']
        res.json({
            msg: "操作成功",
            status: 200,
            allCount,
            datas: data[1]
        });
    }, err => {
        res.json({
            msg: "数据为空",
            status: 500,
            datas: [],
            err: err
        });
    });
});

// 导出当前查询的数据为excel文件，返回文件地址
router.get('/exportExcel', async function(req, res, next) {
    res.header("Content-Type", "application/json; charset=utf-8")

    let param = ''
    if (req.method == "POST") {
        param = req.body
    } else {
        param = req.query || req.params
    }
    console.log(req.query, req.params)
    let {
        cid,
        pname,
        stime,
        etime
    } = param

    if (!stime || !etime) {
        stime = ''
        etime = ''
    }

    if (!param.cid) {
        res.end(JSON.stringify({
            msg: '请传入职位分类cid',
            status: '102'
        }));
        return;
    }

    let where = ''
    let plistItem = await db.first('SELECT * FROM position_list WHERE id = ?', [param.cid])
    let searchKeyWords = plistItem["name"]
    where +=
        searchKeyWords !== '' ?
        ` WHERE searchKeyWords = '${searchKeyWords}'` : ''
    where += pname && pname !== '' ?
        ` AND positionName LIKE '%${pname}%'` : ''
    where += stime !== '' && etime !== '' ?
        ` AND createTime BETWEEN '${stime}' AND '${etime}'` : ''
    console.log(where);

    // 提供前端当前查询条件下的所有数据，方便导出excel
    let exportSql = `SELECT 
    * FROM job_list
    ${where}
    GROUP BY positionId`
    console.log(exportSql)
    let exportData = await db.row(exportSql)
    // 导出后的文件地址
    excelManger.exportExcel(exportData, searchKeyWords).then(data => {
        res.json({
            msg: "操作成功",
            status: 200,
            downloadURL: data
        });
    }, err => {
        res.json({
            msg: "数据为空",
            status: 500,
            downloadURL: '',
            err: err
        });
    })
})

router.get('/test', async function (req, res, next) {
    res.header("Content-Type", "application/json; charset=utf-8")
    db.row(`SELECT description FROM job_detail LIMIT 100`).then(data => {
        let sentence = ''
        for (const desc of data) {
            sentence += desc.description
        }
        res.json({
            msg: "操作成功",
            status: 200,
            datas: sentence
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

router.get('/plist', function (req, res, next) {
    res.header("Content-Type", "application/json; charset=utf-8")

    db.row('SELECT * FROM position_list').then( data => {
        console.log(data)
        res.json({
            msg: "操作成功",
            status: 200,
            datas: data
        });
    }, err => {
        console.log(err)
        res.json({
            msg: "数据为空",
            status: 500,
            datas: []
        });
    });
})

module.exports = router;