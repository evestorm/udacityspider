var nodeExcel = require('excel-export');
const fs = require('fs')

let excelConf = {}

let cols = [
    {
        caption: '公司ID',
        type: 'number',
    },
    {
        caption: '工作经验',
        type: 'string',
    },
    {
        caption: '教育程度',
        type: 'string',
    },
    {
        caption: '工作性质',
        type: 'string',
    },
    {
        caption: '岗位名称',
        type: 'string',
    },
    {
        caption: '岗位ID',
        type: 'number',
    },
    {
        caption: '发布时间',
        type: 'string',
    },
    {
        caption: '城市',
        type: 'string',
    },
    {
        caption: '公司LOGO',
        type: 'string',
    },
    {
        caption: '工业领域',
        type: 'string',
    },
    {
        caption: '岗位优势',
        type: 'string',
    },
    {
        caption: '薪资',
        type: 'string',
    },
    {
        caption: '公司规模',
        type: 'string',
    },
    {
        caption: '公司简称',
        type: 'string',
    },
    {
        caption: '岗位标签',
        type: 'string',
    },
    {
        caption: '融资阶段',
        type: 'string',
    },
    {
        caption: '公司标签',
        type: 'string',
    },
    {
        caption: '经度',
        type: 'string',
    },
    {
        caption: '纬度',
        type: 'string',
    },
    {
        caption: '公司全称',
        type: 'string',
    },
    {
        caption: '一级分类',
        type: 'string',
    },
    {
        caption: '二级分类',
        type: 'string',
    },
    {
        caption: '是否实习',
        type: 'number',
    },
    {
        caption: '三级分类',
        type: 'string',
    },
    {
        caption: '技能标签',
        type: 'string',
    }
]

/**
 * 导出数据为excel文件
 * @param {arry} data 数组形式data
 * @param {string} positionName 职位名称，导出文件名用
 */

// 资料借鉴： https: //www.jianshu.com/p/ba2294402aa8
let exportExcel = (data, positionName) => {
    let excelConf = {
        cols: cols,
        rows: []
    }
    let temp = []
    for (let i = 0; i < data.length; i++) {
        // 获取每个职位对象
        const p = data[i];
        let buffer = [p.companyId, p.workYear, p.education, p.jobNature, p.positionName, p.positionId, p.createTime, p.city, p.companyLogo, p.industryField, p.positionAdvantage, p.salary, p.companySize, p.companyShortName, p.positionLables, p.financeStage, p.companyLabelList, p.longitude, p.latitude, p.companyFullName, p.firstType, p.secondType, p.isSchoolJob, p.thirdType, p.skillLables]
        temp.push(buffer)
    }

    excelConf.rows = temp

    var result = nodeExcel.execute(excelConf);
    var random = Math.floor(Math.random() * 10000 + 0); //用来保证生成不同的文件名
    var uploadDir = './public/upload/';
    var filePath = uploadDir + positionName + ".xlsx"; //文件名

    return new Promise(function (resolve, reject) {
        fs.writeFile(filePath, result, 'binary', function (err) {
            if (err) {
                reject(err);
                console.log(err)
                return;
            }
            resolve('http://localhost:3000/upload/' + positionName + ".xlsx");
        });
    })
}

module.exports = {
    cols,
    exportExcel
}


// const tableLabelMap = {
//             id: 'ID',
//             companyId: '公司ID',
//             workYear: '工作经验',
//             education: '教育程度',
//             jobNature: '工作性质',
//             positionName: '岗位名称',
//             positionId: '岗位ID',
//             createTime: '发布时间',
//             city: '城市',
//             companyLogo: '公司LOGO',
//             industryField: '工业领域',
//             positionAdvantage: '岗位优势',
//             salary: '薪资',
//             companySize: '公司规模',
//             companyShortName: '公司简称',
//             positionLables: '岗位标签',
//             financeStage: '融资阶段',
//             companyLabelList: '公司标签',
//             longitude: '经度',
//             latitude: '纬度',
//             companyFullName: '公司全称',
//             firstType: '一级分类',
//             secondType: '二级分类',
//             isSchoolJob: '是否实习',
//             thirdType: '三级分类',
//             skillLables: '技能标签',
//             searchKeyWords: '搜索关键词'
//         }