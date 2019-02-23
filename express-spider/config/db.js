'use strict';
const mysql = require("mysql");

let pool = mysql.createPool({
    host: "localhost",
    port: 8889,
    user: "root",
    password: "root",
    database: "lagou_job",
    multipleStatements: true // 是否允许执行多条sql
});
// NodeJS MySql 执行多条sql语句
// 设置 multipleStatements 属性为 true
// https://www.cnblogs.com/hzj680539/p/8032270.html

//将结果已对象数组返回
let row = (sql, ...params) => {
    return new Promise(function (resolve, reject) {
        pool.getConnection(function (err, connection) {
            if (err) {
                reject(err);
                return;
            }
            connection.query(sql, params, function (error, res) {
                connection.release();
                if (error) {
                    reject(error);
                    return;
                }
                resolve(res);
            });
        });
    });
};

//返回一个对象
var first = (sql, ...params) => {
    return new Promise(function (resolve, reject) {
        pool.getConnection(function (err, connection) {
            if (err) {
                reject(err);
                return;
            }
            // connection.query('select * from table where age=? and tel in (?);', [20, [1, 2, 3]], function () {})
            connection.query(sql, params, function (error, res) {
                connection.release();
                if (error) {
                    reject(error);
                    return;
                }
                resolve(res[0] || null);
            });
        });
    });
};


//返回单个查询结果
var single = (sql, ...params) => {
    return new Promise(function (resolve, reject) {
        pool.getConnection(function (err, connection) {
            if (err) {
                reject(err);
                return;
            }
            connection.query(sql, params, function (error, res) {
                connection.release();
                if (error) {
                    reject(error);
                    return;
                }
                for (let i in res[0]) {
                    resolve(res[0][i] || null);
                    return;
                }
                resolve(null);
            });
        });
    });
}

//执行代码，返回执行结果
var execute = (sql, ...params) => {
    return new Promise(function (resolve, reject) {
        pool.getConnection(function (err, connection) {
            if (err) {
                reject(err);
                return;
            }
            connection.query(sql, params, function (error, res) {
                connection.release();
                if (error) {
                    reject(error);
                    return;
                }
                resolve(res);
            });
        });
    });
}

//模块导出
module.exports = {
    row,
    first,
    single,
    execute
}

// const mysql = require('./mysql.js');

// (async () => {
//     let s = await mysql.row(sql, params);
//     console.log(s);
// })();


// function query(sql, callback) {
//     pool.getConnection(function (err, connection) {
//         connection.query(sql, function (err, rows) {
//             callback(err, rows);
//             connection.release();
//         });
//     });
// }

// exports.query = query;