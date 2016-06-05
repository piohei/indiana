var DEBUG = false;
var currentPosition = { x: 0, y: 0, z: 0 };

var camera, controls, scene, renderer;
var rooms, lights, locator;

var lightColor = "#ffffff";
var lightIntensity = 1;
var blockColor = "#330099";
var locatorColor = "#b60000";
var routerColor = "#00bb00";

var ws = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/websocket");
ws.onmessage = function (evt) {
    received = evt.data.split(":").map( function (v) { return parseInt(v) } );
    currentPosition.x = received[0];
    currentPosition.y = received[1];
    currentPosition.z = received[2];
};

// 1 == 1m in real world (just for scale)
var roomsInput = [
    { left_bottom: {x: 10, y: 10}, right_up: {x: 30, y: 35} },
    { left_bottom: {x: 10, y: -40}, right_up: {x: 50, y: 10} }
];

var routersInput = [
    {x: 10, y: 10},
    {x: 30, y: 35},
];

function init() {
    camera = new THREE.PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 1, 2000 );
    // camera = new THREE.OrthographicCamera(-100, 100, 100, -100, 1, 1000);
    camera.position.z = 50;
    camera.position.y = 20;
    camera.position.x = 50;

    camera.lookAt(new THREE.Vector3(0,0,0));

    runControls();
    debugHelpers();

    generateLocator();
    locator.position.set(20, 0, 20);
    generateMap();

    generateScene();

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );

    document.body.appendChild( renderer.domElement );
    window.addEventListener( 'resize', onWindowResize, false );
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );
    if(controls != null) controls.handleResize();

    render();
}

function animate() {
    requestAnimationFrame( animate );
    locator.position.x = 20 + currentPosition.x / 10;
    if(controls != null) controls.update();
    render();
}

function render() {
    renderer.render( scene, camera );
}

// Helpers

// Locator height is 1.8
function generateLocator() {
    var headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
    var bodyGeometry = new THREE.CylinderGeometry(0.1, 0.3, 1.7, 36);
    var material = new THREE.MeshLambertMaterial( { color: 0xff0000 } );

    headGeometry.translate(0, 1.7, 0);
    bodyGeometry.translate(0, 1.7 / 2, 0);
    headGeometry.merge(bodyGeometry);

    locator = new THREE.Mesh( headGeometry, material);
}

function generateMap() {
    rooms = [];
    lights = [];
    routers = [];
    wallHeight = 2.5;

    roomsInput.forEach(function(room) {
        var width = room.right_up.x - room.left_bottom.x;
        var height = room.right_up.y - room.left_bottom.y;

        var floorGeometry = new THREE.BoxGeometry(width, 0.01, height);
        var wallWidth1Geometry = new THREE.BoxGeometry(width + 0.02, wallHeight, 0.02);
        var wallWidth2Geometry = new THREE.BoxGeometry(width + 0.02, wallHeight, 0.02);
        var wallHeight1Geometry = new THREE.BoxGeometry(0.02, wallHeight, height + 0.02);
        var wallHeight2Geometry = new THREE.BoxGeometry(0.02, wallHeight, height + 0.02);
        var material = new THREE.MeshLambertMaterial({ color: blockColor });

        floorGeometry.translate(width / 2, 0, height / 2);
        floorGeometry.translate(room.left_bottom.x, -0.005, room.left_bottom.y);

        wallWidth1Geometry.translate(width / 2 + 0.01, 0, 0.01);
        wallWidth2Geometry.translate(width / 2 + 0.01, 0, 0.01);
        wallWidth1Geometry.translate(room.left_bottom.x, wallHeight / 2, room.left_bottom.y);
        wallWidth2Geometry.translate(room.left_bottom.x, wallHeight / 2, room.right_up.y);

        wallHeight1Geometry.translate(0.01, 0, height / 2 + 0.01);
        wallHeight2Geometry.translate(0.01, 0, height / 2 + 0.01);
        wallHeight1Geometry.translate(room.left_bottom.x, wallHeight / 2, room.left_bottom.y);
        wallHeight2Geometry.translate(room.right_up.x, wallHeight / 2, room.left_bottom.y);

        rooms.push({
            floor: new THREE.Mesh( floorGeometry, material ),
            walls: [
                new THREE.Mesh( wallWidth1Geometry, material ),
                new THREE.Mesh( wallWidth2Geometry, material ),
                new THREE.Mesh( wallHeight1Geometry, material ),
                new THREE.Mesh( wallHeight2Geometry, material )
            ]
        });

        var light = new THREE.PointLight(lightColor, lightIntensity, Math.max(width, height) * 10);

        light.position.set(
            (room.left_bottom.x + room.right_up.x) / 2,
            Math.max(width, height) / 2,
            (room.left_bottom.y + room.right_up.y) / 2
        );

        if(DEBUG) {
            var lightGeometry = new THREE.SphereGeometry(1, 16, 16);
            var lightMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
            light.add(new THREE.Mesh(lightGeometry, lightMaterial));
        }

        lights.push(light);
    });

    routersInput.forEach(function(router) {
        var geometry = new THREE.SphereGeometry(0.3, 16, 16);
        var material = new THREE.MeshLambertMaterial({ color: routerColor });

        geometry.translate(router.x, wallHeight, router.y);

        routers.push(new THREE.Mesh(geometry, material));
    });
}

function generateScene() {
    scene = new THREE.Scene();

    scene.add( locator );

    rooms.forEach(function (room) {
        scene.add(room.floor);
        room.walls.forEach(function (wall) {
            scene.add(wall);
        });
    });
    lights.forEach(function (light) {
        scene.add(light);
    });
    routers.forEach(function (light) {
        scene.add(light);
    });
}

function runControls() {
    if(DEBUG) {
        return;
    }

    controls = new THREE.TrackballControls( camera );

    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.0;
    controls.panSpeed = 1.0;

    controls.noZoom = false;
    controls.noPan = false;

    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;

    controls.keys = [ 65, 83, 68 ];

    controls.addEventListener( 'change', render );
}

function debugHelpers() {
    if(!DEBUG) {
        return;
    }

    var guiControls = new function () {
        this.lightColor = lightColor;
        this.lightIntensity = lightIntensity;
        this.blockColor = blockColor;
        this.locatorColor = locatorColor;
        this.routerColor = routerColor;
    }

    var gui = new dat.GUI();

    gui.addColor(guiControls, 'lightColor').onChange(function (e) {
        lights.forEach(function(item) {
            item.color = new THREE.Color(e);
        });
    });

    gui.add(guiControls, 'lightIntensity', 0, 5).onChange(function (e) {
        lights.forEach(function(item) {
            item.intensity = e;
        });
    });

    gui.addColor(guiControls, 'blockColor').onChange(function (e) {
        boxes.forEach(function (item) {
            item.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
        });
        floorMesh.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
    });

    gui.addColor(guiControls, 'locatorColor').onChange(function (e) {
        locator.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
    });

    gui.addColor(guiControls, 'routerColor').onChange(function (e) {
        routers.forEach(function (item) {
            item.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
        });
    });
}
