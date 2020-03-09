const sqlite3 = require('sqlite3').verbose()
const firebase = require('firebase')

let config = {
  // firebase config
}
var fire = firebase.initializeApp(config);

let db = new sqlite3.Database('db.sqlite3', sqlite3.OPEN_READONLY, err => {
  if (err) {
    console.log(err)
  }
})

const fs = fire.firestore()

let sql = `SELECT r.*, c.name as 'cat_name'
            FROM homepage_recipe r
              JOIN homepage_category c
                ON c.id = r.category_id`


let users = {
  1: 'some_ID',
  2: 'some_other_ID'
}

db.all(sql, [], (err, rows) => {
  if (err) {
    throw err
  }

  rows.forEach((row, idx) => {
    let newRecipe = {
      name: row.name,
      ingredients: row.ingredients.replace(/\r\n/g, "<SEP>"),
      directions: row.steps.replace(/\r\n/g, "<SEP>"),
      category: row.cat_name,
      notes: row.notes.replace(/\r\n/g, "<SEP>"),
      img_path: row.image_link,
      orig_link: row.link,
      uid: users[row.owner_id],
      create_date: new Date(row.create_date).getTime(),
      modify_date: new Date(row.last_modified).getTime()
    }

    fs.collection('recipes').add(newRecipe)
      .then(res => {
        console.log(`added recipe (${idx+1})`)
      })
      .catch(err => {
        console.log(err)
      })
  })
})