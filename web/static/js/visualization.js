VISUALIZATION = (function() {
    var DEBUG = false;
    var currentPosition = { x: 0, y: 0, z: 0 };

    var camera, controls, scene, renderer;
    var floors, lights, locator;

    var type, engine;

    ENGINE = (function() {
        function initEngine2D() {
            console.log("Initalizing 2D engine.");
            var floorColor = "#ffffff";
            var wallColor  = "#000000";
            var locatorColor = "#ff0000";
            var routerColor = "#239123";

            function initCamera() {
                console.log("New camera.");
                camera = new THREE.OrthographicCamera(
                    window.innerWidth / -2 / 30,
                    window.innerWidth / 2 / 30,
                    window.innerHeight / 2 / 30,
                    window.innerHeight / -2 / 30,
                    -500,
                    1000
                );

                camera.position.x = 16.5;
                camera.position.y = -6;
                camera.position.z = 10;

                camera.rotation.x = 0;
                camera.rotation.y = 0;
                camera.rotation.z = 0;
            }

            // Locator height is 1.8
            function generateLocator() {
                var headGeometry = new THREE.CircleGeometry(0.2, 32);
                var material = new THREE.MeshBasicMaterial({
                    color: locatorColor,
                });

                headGeometry.translate(0, 0, 0.2);

                locator = new THREE.Mesh(headGeometry, material);
            }

            function generateFloor(vertices) {
                var floorShape = new THREE.Shape();

                floorShape.moveTo(
                    vertices[vertices.length - 1].x,
                    vertices[vertices.length - 1].y
                );

                vertices.forEach(function(vertex) {
                    floorShape.lineTo(vertex.x, -1 * vertex.y);
                });

                var material = new THREE.MeshBasicMaterial({
                    color: floorColor,
                });

                var floorShapeGeometry = new THREE.ShapeGeometry(floorShape);

                floorShapeGeometry.translate(0, 0, -0.1);

                return new THREE.Mesh(floorShapeGeometry, material);
            }

            function generateWall(wall) {
                var geometry = new THREE.Geometry();
                geometry.vertices.push(
                    new THREE.Vector3(wall.start.x, -1 * wall.start.y, 0),
                    new THREE.Vector3(wall.end.x, -1 * wall.end.y, 0)
                );

                var material = new THREE.LineBasicMaterial({
                    color: wallColor,
                    linewidth: 1,
                });

                return new THREE.Line(geometry, material);
            }

            function generateRouter(router) {
                var geometry = new THREE.CircleGeometry(0.10, 32);

                var material = new THREE.MeshBasicMaterial({
                    color: routerColor,
                });

                geometry.translate(router.x, -1 * router.y, 0.1);

                return new THREE.Mesh(geometry, material);
            }

            function generateLights() {

            }

            function runControls() {
                if(DEBUG) {
                    return;
                }

                console.log("Running controls.");

                controls = new THREE.OrthographicTrackballControls( camera );

                controls.rotateSpeed = 1.0;
                controls.zoomSpeed = 1.0;
                controls.panSpeed = 1.0;

                controls.noZoom = false;
                controls.noPan = false;
                controls.noRotate = true;
                controls.noRoll = true;

                controls.target = new THREE.Vector3(16.5, -6, 0);

                controls.staticMoving = true;
                controls.dynamicDampingFactor = 0.3;

                controls.keys = [ 65, 83, 68 ]; // a, s, d

                controls.addEventListener( 'change', render );
            }

            function debugHelpers() {
                if(!DEBUG) {
                    return;
                }

                var guiControls = new function () {
                    this.lightColor = lightColor;
                    this.lightIntensity = lightIntensity;
                    this.floorColor = floorColor;
                    this.wallColor = wallColor;
                    this.locatorColor = locatorColor;
                    this.routerColor = routerColor;
                };

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

                gui.addColor(guiControls, 'floorColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.floor.material = new THREE.MeshLambertMaterial({
                            color: new THREE.Color(e),
                            emissive: new THREE.Color(e),
                        });
                    });
                });

                gui.addColor(guiControls, 'wallColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.walls.forEach(function (wall) {
                            wall.material = new THREE.MeshLambertMaterial({
                                color: new THREE.Color(e),
                                emissive: new THREE.Color(e),
                                side: THREE.DoubleSide
                            });
                        });
                    });
                });

                gui.addColor(guiControls, 'locatorColor').onChange(function (e) {
                    locator.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
                });

                gui.addColor(guiControls, 'routerColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.routers.forEach(function (router) {
                            router.material = new THREE.MeshLambertMaterial({
                                color: new THREE.Color(e),
                                emissive: new THREE.Color(e)
                            });
                        });
                    });
                });
            }

            return {
                initCamera: initCamera,
                generateLocator: generateLocator,
                generateFloor: generateFloor,
                generateWall: generateWall,
                generateRouter: generateRouter,
                generateLights: generateLights,
                runControls: runControls,
                debugHelpers: debugHelpers,
            }
        }

        function initEngine3D() {
            console.log("Initalizing 3D engine.");
            var lightColor = "#ffffff";
            var lightIntensity = 0.4;
            var floorColor = "#3800aa";
            var wallColor  = "#5c018e";
            var locatorColor = "#ff0000";
            var routerColor = "#239123";

            var wallHeight = 2.5;
            var wallThickness = 0.02;

            function initCamera() {
                console.log("New camera.");
                camera = new THREE.PerspectiveCamera(
                    60,
                    window.innerWidth / window.innerHeight,
                    1,
                    2000
                );

                camera.position.x = 20;
                camera.position.y = 10;
                camera.position.z = 20;

                camera.rotation.x = 0;
                camera.rotation.y = 0;
                camera.rotation.z = 0;

                debugHelpers();
            }

            // Locator height is 1.8
            function generateLocator() {
                var headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
                var bodyGeometry = new THREE.CylinderGeometry(0.1, 0.3, 1.7, 36);

                headGeometry.translate(0, 1.7, 0);
                bodyGeometry.translate(0, 1.7 / 2, 0);
                headGeometry.merge(bodyGeometry);

                var material = new THREE.MeshLambertMaterial({
                    color: locatorColor,
                    emissive: locatorColor,
                });

                locator = new THREE.Mesh(headGeometry, material);
            }

            function generateFloor(vertices) {
                var floorShape = new THREE.Shape();

                floorShape.moveTo(
                    vertices[vertices.length - 1].x,
                    vertices[vertices.length - 1].y
                );

                vertices.forEach(function(vertex) {
                    floorShape.lineTo(vertex.x, vertex.y);
                });

                var material = new THREE.MeshLambertMaterial({
                    color: floorColor,
                    emissive: floorColor
                });

                var floorShapeGeometry = floorShape.extrude({
                    amount: 0.02,
                    bevelEnabled: false
                }).rotateX( Math.PI / 2);

                return new THREE.Mesh(floorShapeGeometry, material);
            }

            function generateWall(wall) {
                width = Math.sqrt(Math.pow(wall.start.x - wall.end.x, 2) +
                                  Math.pow(wall.start.y - wall.end.y, 2));
                arc = Math.atan2(wall.start.y - wall.end.y, wall.end.x - wall.start.x);

                wallGeometry = new THREE.PlaneGeometry(width, wallHeight).
                                    translate(width / 2, wallHeight / 2, 0).
                                    rotateY(arc).
                                    translate(wall.start.x, 0, wall.start.y);

                var material = new THREE.MeshLambertMaterial({
                    color: wallColor,
                    emissive: wallColor,
                    side: THREE.DoubleSide
                });

                return new THREE.Mesh( wallGeometry, material );
            }

            function generateRouter(router) {
                var geometry = new THREE.SphereGeometry(0.10, 16, 16);

                var material = new THREE.MeshLambertMaterial({
                    color: routerColor,
                    emissive: routerColor
                });

                geometry.translate(router.x, wallHeight, router.y);

                return new THREE.Mesh(geometry, material);
            }

            function generateLights() {
                // Direct light
                var light = new THREE.DirectionalLight(lightColor, lightIntensity);
                light.position.set(0.0, 0.0, 10.0).normalize();
                lights.push(light)
                scene.add(light);

                // Ambient light
                var ambientLight = new THREE.AmbientLight(lightColor, lightIntensity);
                lights.push(ambientLight)
                scene.add(ambientLight);
            }


            function runControls() {
                if(DEBUG) {
                    return;
                }

                console.log("Running controls.");

                controls = new THREE.TrackballControls( camera );

                controls.rotateSpeed = 1.0;
                controls.zoomSpeed = 1.0;
                controls.panSpeed = 1.0;

                controls.noZoom = false;
                controls.noPan = false;

                controls.staticMoving = true;
                controls.dynamicDampingFactor = 0.3;

                controls.keys = [ 65, 83, 68 ]; // a, s, d

                controls.addEventListener( 'change', render );
            }

            function debugHelpers() {
                if(!DEBUG) {
                    return;
                }

                var guiControls = new function () {
                    this.lightColor = lightColor;
                    this.lightIntensity = lightIntensity;
                    this.floorColor = floorColor;
                    this.wallColor = wallColor;
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

                gui.addColor(guiControls, 'floorColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.floor.material = new THREE.MeshLambertMaterial({
                            color: new THREE.Color(e),
                            emissive: new THREE.Color(e),
                        });
                    });
                });

                gui.addColor(guiControls, 'wallColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.walls.forEach(function (wall) {
                            wall.material = new THREE.MeshLambertMaterial({
                                color: new THREE.Color(e),
                                emissive: new THREE.Color(e),
                                side: THREE.DoubleSide
                            });
                        });
                    });
                });

                gui.addColor(guiControls, 'locatorColor').onChange(function (e) {
                    locator.material = new THREE.MeshLambertMaterial( { color: new THREE.Color(e) } );
                });

                gui.addColor(guiControls, 'routerColor').onChange(function (e) {
                    floors.forEach(function (floor) {
                        floor.routers.forEach(function (router) {
                            router.material = new THREE.MeshLambertMaterial({
                                color: new THREE.Color(e),
                                emissive: new THREE.Color(e)
                            });
                        });
                    });
                });
            }

            return {
                initCamera: initCamera,
                generateLocator: generateLocator,
                generateFloor: generateFloor,
                generateWall: generateWall,
                generateRouter: generateRouter,
                generateLights: generateLights,
                runControls: runControls,
                debugHelpers: debugHelpers,
            }
        }

        function initEngine(type) {
            switch(type) {
                case "2D":
                    return initEngine2D();
                case "3D":
                    return initEngine3D();
                default:
                    return initEngine2D();
            }
        }

        return {
            initEngine: initEngine,
        }
    }());


    function init(_type) {
        type = _type;
        var ws = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/position/11-12-13-14-15-16");
        ws.onmessage = function (evt) {
            received = evt.data.split(":").map( function (v) { return parseFloat(v) } );
            if(type == "3D") {
                currentPosition.x = received[0];
                currentPosition.z = received[1];
                currentPosition.y = received[2];
            } else {
                currentPosition.x = received[0];
                currentPosition.y = -received[1];
                currentPosition.z = received[2];
            }
            console.log(currentPosition);
        };
        ws.onopen = function (evt) {
            ws.send("start");
        }
    }

    function run() {
        engine = ENGINE.initEngine(type);

        engine.initCamera();

        engine.debugHelpers();

        generateMap(mapGenerateCallback);
    }

    function mapGenerateCallback() {
        generateScene();

        renderer = new THREE.WebGLRenderer();
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.setSize( window.innerWidth, window.innerHeight );

        engine.runControls();

        document.body.appendChild( renderer.domElement );
        window.addEventListener( 'resize', onWindowResize, false );

        animate();
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

        locator.position.x = currentPosition.x;
        locator.position.y = currentPosition.y;
        locator.position.z = currentPosition.z;

        if(controls != null) controls.update();

        render();
    }

    function render() {
        renderer.render( scene, camera );
    }

    function generateMap(callback) {
        floors = [];
        lights = [];
        routers = [];

        $.getJSON("/map").done(function (data) {
            floor = engine.generateFloor(data.floors[1].floor);

            walls = [];
            data.floors[1].walls.forEach(function(wall) {
                walls.push(engine.generateWall(wall));
            });

            routers = [];
            data.floors[1].routers.forEach(function(router) {
                routers.push(engine.generateRouter(router));
            });

            floors.push({
                floor: floor,
                walls: walls,
                routers: routers
            });

            engine.generateLocator();

            callback();
        }).fail(function (data) {
            alert("Error while getting map!");
        });
    }

    function generateScene() {
        scene = new THREE.Scene();

        // TODO: generate light
        engine.generateLights();

        // Scene elements
        scene.add( locator );

        floors.forEach(function (floor) {
            scene.add(floor.floor);

            floor.walls.forEach(function (wall) {
                scene.add(wall);
            });

            floor.routers.forEach(function (light) {
                scene.add(light);
            });
        });

        locator.position.x = currentPosition.x;
        locator.position.y = currentPosition.y;
        locator.position.z = currentPosition.z;
    }

    FINGERTIP_VISUALIZATION = (function() {

        var floorColor = "#ffffff";
        var wallColor  = "#000000";
        var locatorColor = "#ff0000";
        var routerColor = "#239123";

        function init() {
            camera = new THREE.OrthographicCamera(
                1000 / -2 / 30,
                1000 / 2 / 30,
                390 / 2 / 30,
                390 / -2 / 30,
                -500,
                1000
            );

            camera.position.x = 16.5;
            camera.position.y = -6;
            camera.position.z = 10;

            camera.rotation.x = 0;
            camera.rotation.y = 0;
            camera.rotation.z = 0;

            generateLocator();

            locator.position.x = currentPosition.x;
            locator.position.y = currentPosition.y;
            locator.position.z = currentPosition.z;

            generateMap(callback = function() {
                generateScene();

                renderer = new THREE.WebGLRenderer({canvas: document.getElementById("map-canvas")});
                renderer.setPixelRatio( window.devicePixelRatio );

                render();
            });
        }

        function render() {
            var fingertip = {};
            try {
                fingertip.x = toNumber($("#x").val());
                fingertip.y = toNumber($("#y").val());
                fingertip.z = toNumber($("#z").val());
            } catch (err) {
                fingertip.x = 0;
                fingertip.y = 0;
                fingertip.z = 0;
            }
            console.log(fingertip);
            locator.position.x = fingertip.x;
            locator.position.y = -fingertip.y;
            locator.position.z = -fingertip.z;
            renderer.render( scene, camera );
        }

        function run() {
            init();
        }

        // Helpers

        // Locator height is 1.8
        function generateLocator() {
            var headGeometry = new THREE.CircleGeometry(0.2, 32);
            var material = new THREE.MeshBasicMaterial({
                color: locatorColor,
            });

            headGeometry.translate(0, 0, 0.2);

            locator = new THREE.Mesh(headGeometry, material);
        }

        function generateFloor(vertices) {
            var floorShape = new THREE.Shape();

            floorShape.moveTo(
                vertices[vertices.length - 1].x,
                vertices[vertices.length - 1].y
            );

            vertices.forEach(function(vertex) {
                floorShape.lineTo(vertex.x, -1 * vertex.y);
            });

            var material = new THREE.MeshBasicMaterial({
                color: floorColor,
            });

            var floorShapeGeometry = new THREE.ShapeGeometry(floorShape);

            floorShapeGeometry.translate(0, 0, -0.1);

            return new THREE.Mesh(floorShapeGeometry, material);
        }

        function generateWall(wall) {
            var geometry = new THREE.Geometry();
            geometry.vertices.push(
                new THREE.Vector3(wall.start.x, -1 * wall.start.y, 0),
                new THREE.Vector3(wall.end.x, -1 * wall.end.y, 0)
            );

            var material = new THREE.LineBasicMaterial({
                color: wallColor,
                linewidth: 1,
            });

            return new THREE.Line(geometry, material);
        }

        function generateRouter(router) {
            var geometry = new THREE.CircleGeometry(0.10, 32);

            var material = new THREE.MeshBasicMaterial({
                color: routerColor,
            });

            geometry.translate(router.x, -1 * router.y, 0.1);

            return new THREE.Mesh(geometry, material);
        }

        function generateMap(callback) {
            floors = [];
            lights = [];
            routers = [];

            $.getJSON("/map").done(function (data) {
                floor = generateFloor(data.floors[1].floor);

                walls = [];
                data.floors[1].walls.forEach(function(wall) {
                    walls.push(generateWall(wall));
                });

                routers = [];
                data.floors[1].routers.forEach(function(router) {
                    routers.push(generateRouter(router));
                });

                floors.push({
                    floor: floor,
                    walls: walls,
                    routers: routers
                });

                callback();
            }).fail(function (data) {
                alert("Error while getting map!");
            });
        }

        function generateScene() {
            scene = new THREE.Scene

            // Scene elements
            scene.add( locator );

            floors.forEach(function (floor) {
                scene.add(floor.floor);

                floor.walls.forEach(function (wall) {
                    scene.add(wall);
                });

                floor.routers.forEach(function (light) {
                    scene.add(light);
                });
            });
        }


        return {
            run: run,
            reload: render
        }
    }());

    return {
        init: init,
        run: run,
        runFingertip: FINGERTIP_VISUALIZATION.run
    }
}());
