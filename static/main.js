canvas = document.getElementById("canvas")
canvas.interval = setInterval(drawGraphic, 50)
let ctx = canvas.getContext("2d");
canvas.height =1020;
canvas.width = 1200;

let data = {'computerInfo': false};
let command = "gameInit new"
let stage = "initGame"
let background = new Image()
let player1 = new Image()
let player2 = new Image()
let cubeBlue = new Image()
let cubeYellow = new Image()
let cubeRed = new Image()
let cubeViolet = new Image()
let infectionMark = new Image()
let outBreakMark = new Image()
let vaccineMark = new Image()
let treatAvailable = new Image()
let buildAvailable = new Image()
let cureAvailable = new Image()
let researchCenter = new  Image()
let doctor1 = new Image()
let doctor2 = new Image()
let doctor3 = new Image()
let moveList = []
let indicator = new Image()
let dy = [-4,-3,-2,-1,0,1,2,3,4,3,2,1,0,-1,-2,-3]
let dx = 0

doctor1.src = "../static/img/doctor1.png"
doctor2.src = "../static/img/doctor2.png"
doctor3.src = "../static/img/doctor3.png"
researchCenter.src = "../static/img/RC.png"
cubeBlue.src = "../static/img/blue.png"
cubeYellow.src = "../static/img/yellow.png"
cubeRed.src = "../static/img/red.png"
cubeViolet.src = "../static/img/violet.png"
background.src = "../static/img/background.png"
player1.src = "../static/img/pawnRed.png"
player2.src = "../static/img/pawnYellow.png"
infectionMark.src = "../static/img/infectionMark.png"
outBreakMark.src = "../static/img/outBreakMark.png"
vaccineMark.src = "../static/img/vaccineMark.png"
treatAvailable.src = "../static/img/treatAvailable.png"
buildAvailable.src = "../static/img/buildAvailable.png"
cureAvailable.src = "../static/img/cureAvailable.png"
indicator.src = "../static/img/indicator.png"
background.onload = function(){
  ctx.drawImage(background,0,0);

}

function drawMoveIndicator(x, y) {
  ctx.drawImage(indicator,x-4,y-27)
}

function drawText(story,x,y){
  let lines = story.split('<n>');
  for (let i = 0; i <lines.length; i++){
    ctx.fillText(lines[i], x, y + (i*17) );
  }
}

function drawOnePlayerCard(X,Y,text1,text2,textColor,backgroundColor) {
  ctx.font =  "15px Arial";
  Y += 720
  ctx.textAlign = "center";
  ctx.fillStyle = backgroundColor;
  ctx.fillRect(X, Y, 120 , 45);
  ctx.fillStyle = textColor;
  ctx.textAlign = "center"
  ctx.fillText(text1, X+60, Y+20);
  ctx.fillText(text2, X+60, Y+35);
}

function drawOneVirusCube(x,y,cube) {
  let l_i = 0
  let cube_xy = [[0,-2],[-8,4],[+8,4],[-16,9],[0,9],[16,9]]
  for (let i = 0; i < cube[0]; i++){
    ctx.drawImage(cubeBlue,x + cube_xy[l_i][0], y + cube_xy[l_i][1])
    l_i += 1
  }
  for (let i = 0; i < cube[1]; i++){
    ctx.drawImage(cubeViolet,x + cube_xy[l_i][0], y + cube_xy[l_i][1])
    l_i += 1
  }
  for (let i = 0; i < cube[2]; i++){
    ctx.drawImage(cubeRed,x + cube_xy[l_i][0], y + cube_xy[l_i][1])
    l_i += 1
  }
  for (let i = 0; i < cube[3]; i++){
    ctx.drawImage(cubeYellow,x + cube_xy[l_i][0], y + cube_xy[l_i][1])
    l_i += 1
  }
}

function drawGraphic(){
  dx = (dx+1)%160
  if (data['computerInfo']){
    ctx.drawImage(background,0,0);
    drawAllPlayerCard(data)
    drawGameInfo(data,-dy[dx%16]*0.5)
    drawAllVirusCube(data)
    drawPlayerPawn(data)
    drawAllMoveIndicator(data,dy[dx%16])
    drawStory(data)
  }
}

function drawPlayerPawn(data){
  if (data['player'][0]['latitude'] === data['player'][1]['latitude']){
    ctx.drawImage(player1, data['player'][0]['latitude']-10, data['player'][0]['longitude']- 25);
    ctx.drawImage(player2, data['player'][1]['latitude'], data['player'][1]['longitude']- 25);
  }
  else{
    ctx.drawImage(player1, data['player'][0]['latitude'], data['player'][0]['longitude']-25);
    ctx.drawImage(player2, data['player'][1]['latitude'], data['player'][1]['longitude']-25);
  }
}

function drawAllPlayerCard(data){
  if (data['own']){
    let order = 0
    data['own'].forEach((item) =>{
      let textColor = 'rgb(0,67,106)';
      let backgroundColor = 'rgb(150,222,255)';
      switch (item['color']){
        case 'blue':{
          textColor = 'rgb(0,67,106)'
          backgroundColor = 'rgb(109,207,246)'
          break
        }
        case 'violet':{
          textColor = 'rgb(58,0,106)'
          backgroundColor = 'rgb(161,134,190)'
          break
        }
        case 'yellow':{
          textColor = 'rgb(106,97,0)'
          backgroundColor = 'rgb(255,247,153)'
          break
        }
        case 'red':{
          textColor = 'rgb(106,0,0)'
          backgroundColor = 'rgb(245,152,157)'
          break
        }
      }
      drawOnePlayerCard(order%4*130+60,Math.floor(order/4)*50+60,item['name'],"("+item['color']+")",textColor,backgroundColor)
      order += 1
    })
  }
}

function drawAllVirusCube(data){
  data['city'].forEach((city) => {
    if(city['blue']+city['red']+city['violet']+city['yellow'] > 0){
      drawOneVirusCube(city['latitude'],city['longitude'],[city['blue'],city['violet'],city['red'],city['yellow']])
    }
    if(city['research_center'] > 0){
      ctx.drawImage(researchCenter,city['latitude']-5,city['longitude']-30)
    }
  })
}

function drawAllMoveIndicator(data,dy) {

    moveList = []
    if (data['action']['move']['jet']) {
      data['city'].forEach((item) => {
        drawMoveIndicator(item['latitude'], item['longitude']+dy)
        moveList.push({
          "id": item["id"],
          "latitude": item['latitude'],
          "longitude": item['longitude']
        })
      })
    } else {
      if (data['action']['move']['drive']) {
        data['action']['move']['drive'].forEach((item) => {
          drawMoveIndicator(item['location'][0], item['location'][1]+dy)
          moveList.push({
            "id": item["id"],
            "latitude": item['location'][0],
            "longitude": item['location'][1]
          })
        })
      }
      if (data['action']['move']['fly']) {
        data['action']['move']['fly'].forEach((item) => {
          drawMoveIndicator(item['location'][0], item['location'][1]+dy)
          moveList.push({
            "id": item["id"],
            "latitude": item['location'][0],
            "longitude": item['location'][1]
          })
        })
      }
      if (data['action']['move']['rc']) {
        data['action']['move']['rc'].forEach((item) => {
          drawMoveIndicator(item['location'][0], item['location'][1]+dy)
          moveList.push({
            "id": item["id"],
            "latitude": item['location'][0],
            "longitude": item['location'][1]
          })
        })
      }
    }

}

function drawGameInfo(data,dy){
  if (data['game']['player_turn'] === 1)
    ctx.drawImage(player1, 110, 730);
  else
    ctx.drawImage(player2, 110, 730);
  ctx.font =  "17px Arial";
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(10,10,10,1)";
  let playerTurn = data['game']['player_turn']
  let actionPoint = data['player'][playerTurn-1]['action_point']
  ctx.fillText("Player " + playerTurn + " turn. "
      + actionPoint + " Action point left. player hand:", 135, 753)

  ctx.drawImage(infectionMark, 34+24*data['game']['infection_track'],538)

  for (let i = 0; i < data['game']['outbreak_track']; i++)
    ctx.drawImage(outBreakMark,48 + 23 * i-14, 468)

  if (data['game']['blue'] === 1)
    ctx.drawImage(vaccineMark,45, 660)
  if (data['game']['violet'] === 1)
    ctx.drawImage(vaccineMark,85, 660)
  if (data['game']['red'] === 1)
    ctx.drawImage(vaccineMark,125, 660)
  if (data['game']['yellow'] === 1)
    ctx.drawImage(vaccineMark,165, 660)
  if ((data['action']['build']))
    ctx.drawImage(buildAvailable,602,844+dy)
  if ((data['action']['treat'][0]+data['action']['treat'][1]+data['action']['treat'][2]+data['action']['treat'][3])>0)
    ctx.drawImage(treatAvailable,602,785+dy)
  if ((data['action']['cure']))
    ctx.drawImage(cureAvailable,602,897+dy)
}

function drawStory(data){
  ctx.font =  "17px Arial";
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(10,10,10,1)";
  let currentEvent = data['computerInfo'][0]
  let checkWinLose = data['computerInfo'][data['computerInfo'].length-1]
  if (checkWinLose['check']){
    if (checkWinLose['check'][0] === "lose"){
      ctx.drawImage(doctor3, 1020,700)
      drawText(checkWinLose['check'][1],765, 750)
    }
    else{
      ctx.drawImage(doctor2, 1020,700)
      drawText(checkWinLose['check'][1],765, 750)
    }
    stage = "endGame"
  }
  else{
    if (currentEvent['eventType'] === 'cardDraw'){
      ctx.drawImage(doctor2, 950,700)
      drawText(currentEvent['story'], 800, 750);
    }
    else if (currentEvent['eventType'] === 'story'){
      ctx.drawImage(doctor2, 1010,700)
      drawText(currentEvent['story'], 760, 750);
    }
    else if (currentEvent['eventType'] === 'infectCity'){
      ctx.drawImage(doctor1, 950,700)
      drawText(currentEvent['story'], 765, 750);
    }
    else if (currentEvent['eventType'] === 'cardDrawEpidemic'){
      ctx.drawImage(doctor3, 1020,700)
      drawText(currentEvent['story'], 765, 750);
    }
  }
}

function checkLegitMove(data,x,y){
  //click on map
  command = "illegalClick"
  moveList.forEach((item)=>{
    let distance = (x-7 - item['latitude'])**2 + (y+17 - item['longitude'])**2
    if (distance < 250){
      command = 'move '+item["id"]
    }
  })
  //treat button
  if (((x-655)**2 + (y-791)**2) <1000){
    for (let i  = 0; i < data['action']['treat'].length; i++)
      if (data['action']['treat'][i] > 0)
        command = 'treat ' + i
  }
  //build button
  if (((x-655)**2 + (y-856)**2) <1000){
    if (data['action']['build']){
      command = 'build rc'
    }
  }
  //cure button
  if (((x-655)**2 + (y-912)**2) <1000){
    if (data['action']['cure']){
      command = 'cure '+ data['action']['cure']['cure'][0]
    }
  }
  //new game button
  if (((x-236)**2 + (y-975)**2) <1000){
    stage = 'gameStage'
    command = "gameInit new"
  }
  //tutorial button
  if (((x-378)**2 + (y-975)**2) <1000){
    stage = 'gameInitTutorial'
    command = "gameInitTutorial new"
  }
  return command
}

canvas.addEventListener('click', async function(event){
  event.preventDefault()
  const x = event.clientX - canvas.getBoundingClientRect().left
  const y = event.clientY - canvas.getBoundingClientRect().top
  if (stage === 'storyStage'){
    if (data['computerInfo'].length === 1){
      command ="Next player"
      let data_obj = await fetch(`/test2?data=${command}`)
      data = await data_obj.json()
      stage = 'gameStage'
    }
    else {
      data['computerInfo'].shift()
    }
  }
  else if (stage === 'gameStage'){
    command = checkLegitMove(data,x,y)
    if (command !== "illegalClick"){
      let data_obj = await fetch(`/test2?data=${command}`)
      data = await data_obj.json()
    }
    if (data['computerInfo'].length > 1){
      stage = 'storyStage'
    }
  }
  else if (stage === 'initGame'){
    let data_obj = await fetch(`/test2?data=${command}`)
    data = await data_obj.json()
    stage = 'storyStage'
  }
  else if (stage === 'gameInitTutorial'){
    command = "gameInitTutorial new"
    let data_obj = await fetch(`/test2?data=${command}`)
    data = await data_obj.json()
    stage = 'storyStage'
  }
  else if (stage === 'endGame')
    command = checkLegitMove(data,x,y)
  console.log(data)
  console.log(stage)
})

