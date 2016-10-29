(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Fingertip = undefined;

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

var _cors = require('./../helpers/cors');

var _logger = require('./../helpers/logger');

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var Fingertip = exports.Fingertip = function () {
  function Fingertip(host, port, elementId) {
    _classCallCheck(this, Fingertip);

    switch (port) {
      case 80:
        this.url = 'http://' + host;
        break;
      case 443:
        this.url = 'https://' + host;
        break;
      default:
        this.url = 'http://' + host + ':' + port;
    }
    this.elementId = elementId;

    this.dataUrl = this.url + '/actual_location';
    this.statusUrl = 'ws://' + host + ':' + port + '/status';

    this.cors = new _cors.CORS();
    this.logger = new _logger.Logger("result");
  }

  _createClass(Fingertip, [{
    key: 'post',
    value: function post() {
      var data = _getData(this);

      if (data != null) {
        var copyThis = this;
        this.cors.post({
          url: copyThis.dataUrl,
          data: data,
          onSuccess: function onSuccess(evt) {
            copyThis.logger.requestSuccess(evt);
          },
          onError: function onError(xhr, err) {
            copyThis.logger.requestError(xhr, err);
          }
        });
      }
    }
  }, {
    key: 'delete',
    value: function _delete() {
      var copyThis = this;
      this.cors.delete({
        url: copyThis.dataUrl,
        onSuccess: function onSuccess(evt) {
          copyThis.logger.requestSuccess(evt);
        },
        onError: function onError(xhr, err) {
          copyThis.logger.requestError(xhr, err);
        }
      });
    }
  }, {
    key: 'getStatus',
    value: function getStatus() {
      this.ws = _createWebSocket(this);
    }
  }, {
    key: 'endStatus',
    value: function endStatus() {
      if (this.ws) {
        this.ws.close();
      }
    }
  }, {
    key: 'clearLog',
    value: function clearLog() {
      this.logger.clear();
    }
  }, {
    key: 'reloadLocation',
    value: function reloadLocation() {
      var data = _getData(this);

      if (data != null) {
        window.currentPosition = data.location;
      }
    }
  }]);

  return Fingertip;
}();

function _getData(_this) {
  var data = { location: {} };

  try {
    data.location.x = _toNumber($('#' + _this.elementId + ' #x').val());
    data.location.y = _toNumber($('#' + _this.elementId + ' #y').val());
    data.location.z = _toNumber($('#' + _this.elementId + ' #z').val());

    data.mac = _toUpperCaseMAC($('#' + _this.elementId + ' #mac').val());
  } catch (err) {
    _this.logger.log(err);
    return null;
  }

  return data;
}

function _createWebSocket(_this) {
  var ws = new WebSocket(_this.statusUrl);

  var elementId = _this.elementId;
  ws.onopen = function (evt) {
    $('#' + elementId + ' #end_status_btn').prop("disabled", false);
    $('#' + elementId + ' #status_btn').prop("disabled", true);
  };

  ws.onmessage = function (evt) {
    _this.logger.log(evt.data);
  };

  ws.onclose = function (evt) {
    $('#' + elementId + ' #end_status_btn').prop("disabled", true);
    $('#' + elementId + ' #status_btn').prop("disabled", false);
  };

  return ws;
}

function _toNumber(x) {
  var n = Number(x);
  if (isNaN(n)) {
    throw 'not a number ' + x;
  }
  return n;
}

function _toUpperCaseMAC(rawMAC) {
  if (!/^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/.test(rawMAC)) {
    throw 'invalid MAC: ' + rawMAC;
  }

  return rawMAC.toUpperCase();
}

},{"./../helpers/cors":2,"./../helpers/logger":3}],2:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var CORS = exports.CORS = function () {
  function CORS() {
    _classCallCheck(this, CORS);
  }

  _createClass(CORS, [{
    key: "post",
    value: function post(params) {
      _doRequest("POST", params);
    }
  }, {
    key: "delete",
    value: function _delete(params) {
      _doRequest("DELETE", params);
    }
  }]);

  return CORS;
}();

function _doRequest(type, params) {
  var request = {
    url: params.url,
    type: type,
    crossDomain: true,
    contentType: 'application/json',
    success: params.onSuccess,
    error: params.onError
  };
  if (params.data) {
    request.data = JSON.stringify(params.data);
  }
  $.ajax(request);
}

},{}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var Logger = exports.Logger = function () {
  function Logger(elementId) {
    _classCallCheck(this, Logger);

    this.elementId = elementId;
  }

  _createClass(Logger, [{
    key: "log",
    value: function log(msg) {
      $("#" + this.elementId).append(msg + "\n");
    }
  }, {
    key: "clear",
    value: function clear() {
      $("#" + this.elementId).text("");
    }
  }, {
    key: "requestSuccess",
    value: function requestSuccess(response) {
      this.log("status: " + response.status + "; message: " + response.data);
    }
  }, {
    key: "requestError",
    value: function requestError(xhr, status) {
      var msg = "status: " + status + "; code: " + xhr.status;
      if (xhr && xhr.responseJSON && xhr.responseJSON.data) {
        msg = msg + ("; message: " + xhr.responseJSON.data);
      }
      this.log(msg);
    }
  }]);

  return Logger;
}();

},{}],4:[function(require,module,exports){
'use strict';

var _map = require('./objects/map');

var _scene = require('./scene/scene');

var _fingertip = require('./fingertip/fingertip');

window.currentPosition = {
  x: 0, y: 0, z: 0
};

window.run = function (type) {
  var elementId = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
  var enableControls = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : true;

  $.getJSON("/map").done(function (map) {
    var scene = new _scene.Scene(type, map, elementId, enableControls);
    scene.show();
  }).fail(function (data) {
    alert("Error while getting map!");
  });
};

window.fingertip = new _fingertip.Fingertip(window.location.hostname, 8887, "fingertip");

},{"./fingertip/fingertip":1,"./objects/map":13,"./scene/scene":18}],5:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Floor = exports.Floor = function (_THREE$Mesh) {
  _inherits(Floor, _THREE$Mesh);

  function Floor(vertices) {
    var color = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "#ffffff";

    _classCallCheck(this, Floor);

    var geometry = _generateGeometry(vertices);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Floor.__proto__ || Object.getPrototypeOf(Floor)).call(this, geometry, material));
  }

  return Floor;
}(THREE.Mesh);

function _generateGeometry(vertices) {
  var floorShape = new THREE.Shape();

  floorShape.moveTo(vertices[vertices.length - 1].x, vertices[vertices.length - 1].y);

  vertices.forEach(function (vertex) {
    floorShape.lineTo(vertex.x, -1 * vertex.y);
  });

  var geometry = new THREE.ShapeGeometry(floorShape);
  geometry.translate(0, 0, -0.1);

  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshBasicMaterial({
    color: color
  });
}

},{}],6:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Locator = exports.Locator = function (_THREE$Mesh) {
  _inherits(Locator, _THREE$Mesh);

  function Locator() {
    var color = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "#ff0000";

    _classCallCheck(this, Locator);

    var geometry = _generateGeometry();
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Locator.__proto__ || Object.getPrototypeOf(Locator)).call(this, geometry, material));
  }

  return Locator;
}(THREE.Mesh);

function _generateGeometry() {
  var headGeometry = new THREE.CircleGeometry(0.2, 32);

  headGeometry.translate(0, 0, 0.2);

  return headGeometry;
}

function _generateMaterial(color) {
  return new THREE.MeshBasicMaterial({
    color: color
  });
}

},{}],7:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Router = exports.Router = function (_THREE$Mesh) {
  _inherits(Router, _THREE$Mesh);

  function Router(position) {
    var height = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2.5;
    var color = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "#239123";

    _classCallCheck(this, Router);

    var geometry = _generateGeometry(position, height);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Router.__proto__ || Object.getPrototypeOf(Router)).call(this, geometry, material));
  }

  return Router;
}(THREE.Mesh);

function _generateGeometry(position, height) {
  var geometry = new THREE.CircleGeometry(0.10, 32);
  geometry.translate(position.x, -1 * position.y, 0.1);
  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color
  });
}

},{}],8:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Wall = exports.Wall = function (_THREE$Line) {
  _inherits(Wall, _THREE$Line);

  function Wall(vertices) {
    var height = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2.5;
    var color = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "#000000";

    _classCallCheck(this, Wall);

    var geometry = _generateGeometry(vertices, height);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Wall.__proto__ || Object.getPrototypeOf(Wall)).call(this, geometry, material));
  }

  return Wall;
}(THREE.Line);

function _generateGeometry(vertices, height) {
  var from = vertices[0];
  var to = vertices[1];

  var geometry = new THREE.Geometry();
  geometry.vertices.push(new THREE.Vector3(from.x, -1 * from.y, 0), new THREE.Vector3(to.x, -1 * to.y, 0));

  return geometry;
}

function _generateMaterial(color) {
  return new THREE.LineBasicMaterial({
    color: color,
    linewidth: 1
  });
}

},{}],9:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Floor = exports.Floor = function (_THREE$Mesh) {
  _inherits(Floor, _THREE$Mesh);

  function Floor(vertices) {
    var color = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "#3800aa";

    _classCallCheck(this, Floor);

    var geometry = _generateGeometry(vertices);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Floor.__proto__ || Object.getPrototypeOf(Floor)).call(this, geometry, material));
  }

  return Floor;
}(THREE.Mesh);

function _generateGeometry(vertices) {
  var floorShape = new THREE.Shape();

  floorShape.moveTo(vertices[vertices.length - 1].x, vertices[vertices.length - 1].y);

  vertices.forEach(function (vertex) {
    floorShape.lineTo(vertex.x, vertex.y);
  });

  return floorShape.extrude({
    amount: 0.02,
    bevelEnabled: false
  }).rotateX(Math.PI / 2);
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color
  });
}

},{}],10:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Locator = exports.Locator = function (_THREE$Mesh) {
  _inherits(Locator, _THREE$Mesh);

  function Locator() {
    var color = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "#ff0000";

    _classCallCheck(this, Locator);

    var geometry = _generateGeometry();
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Locator.__proto__ || Object.getPrototypeOf(Locator)).call(this, geometry, material));
  }

  return Locator;
}(THREE.Mesh);

function _generateGeometry() {
  var headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
  var bodyGeometry = new THREE.CylinderGeometry(0.1, 0.3, 1.7, 36);

  headGeometry.translate(0, 1.7, 0);
  bodyGeometry.translate(0, 1.7 / 2, 0);
  headGeometry.merge(bodyGeometry);

  return headGeometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color
  });
}

},{}],11:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Router = exports.Router = function (_THREE$Mesh) {
  _inherits(Router, _THREE$Mesh);

  function Router(position) {
    var height = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2.5;
    var color = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "#239123";

    _classCallCheck(this, Router);

    var geometry = _generateGeometry(position, height);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Router.__proto__ || Object.getPrototypeOf(Router)).call(this, geometry, material));
  }

  return Router;
}(THREE.Mesh);

function _generateGeometry(position, height) {
  var geometry = new THREE.SphereGeometry(0.1, 16, 16);
  geometry.translate(position.x, height - 0.1, position.y);
  return geometry;
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color
  });
}

},{}],12:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Wall = exports.Wall = function (_THREE$Mesh) {
  _inherits(Wall, _THREE$Mesh);

  function Wall(vertices) {
    var height = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2.5;
    var color = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "#5c018e";

    _classCallCheck(this, Wall);

    var geometry = _generateGeometry(vertices, height);
    var material = _generateMaterial(color);

    return _possibleConstructorReturn(this, (Wall.__proto__ || Object.getPrototypeOf(Wall)).call(this, geometry, material));
  }

  return Wall;
}(THREE.Mesh);

function _generateGeometry(vertices, height) {
  var from = vertices[0];
  var to = vertices[1];

  var width = Math.sqrt(Math.pow(from.x - to.x, 2) + Math.pow(from.y - to.y, 2));
  var arc = Math.atan2(from.y - to.y, to.x - from.x);

  return new THREE.PlaneGeometry(width, height).translate(width / 2, height / 2, 0).rotateY(arc).translate(from.x, 0, from.y);
}

function _generateMaterial(color) {
  return new THREE.MeshLambertMaterial({
    color: color,
    emissive: color,
    side: THREE.DoubleSide
  });
}

},{}],13:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Map = undefined;

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

var _map_level = require('./map_level');

var _locator = require('./2d/locator');

var _locator2 = require('./3d/locator');

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var Map = exports.Map = function () {
  function Map(type, map) {
    _classCallCheck(this, Map);

    this.type = type;
    this.levels = _generateLevels(type, map);
    this.locator = _genreateLocator(type);
  }

  _createClass(Map, [{
    key: 'getLevels',
    value: function getLevels() {
      return this.levels;
    }
  }, {
    key: 'getLocator',
    value: function getLocator() {
      return this.locator;
    }
  }]);

  return Map;
}();

function _generateLevels(type, map) {
  var levels = {};

  for (var level in map.levels) {
    levels[level] = new _map_level.MapLevel(type, map.levels[level]);
  }

  return levels;
}

function _genreateLocator(type) {
  switch (type) {
    case '2d':
      return new _locator.Locator();
    case '3d':
      return new _locator2.Locator();
  }
}

},{"./2d/locator":6,"./3d/locator":10,"./map_level":14}],14:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.MapLevel = undefined;

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

var _floor = require('./2d/floor');

var _wall = require('./2d/wall');

var _router = require('./2d/router');

var _floor2 = require('./3d/floor');

var _wall2 = require('./3d/wall');

var _router2 = require('./3d/router');

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var MapLevel = exports.MapLevel = function () {
  function MapLevel(type, level) {
    _classCallCheck(this, MapLevel);

    this.floor = _generateFloor(type, level.floor);
    this.walls = _generateWalls(type, level.walls);
    this.routers = _generateRouters(type, level.routers);
  }

  _createClass(MapLevel, [{
    key: 'getFloor',
    value: function getFloor() {
      return this.floor;
    }
  }, {
    key: 'getWalls',
    value: function getWalls() {
      return this.walls;
    }
  }, {
    key: 'getRouters',
    value: function getRouters() {
      return this.routers;
    }
  }]);

  return MapLevel;
}();

function _generateFloor(type, floor) {
  switch (type) {
    case '2d':
      return new _floor.Floor(floor);
    case '3d':
      return new _floor2.Floor(floor);
  }
}

function _generateWall(type, wall) {
  switch (type) {
    case '2d':
      return new _wall.Wall(wall);
    case '3d':
      return new _wall2.Wall(wall);
  }
}

function _generateRouter(type, router) {
  switch (type) {
    case '2d':
      return new _router.Router(router);
    case '3d':
      return new _router2.Router(router);
  }
}

function _generateWalls(type, walls) {
  var res = [];
  var _iteratorNormalCompletion = true;
  var _didIteratorError = false;
  var _iteratorError = undefined;

  try {
    for (var _iterator = walls[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
      var wall = _step.value;

      res.push(_generateWall(type, wall));
    }
  } catch (err) {
    _didIteratorError = true;
    _iteratorError = err;
  } finally {
    try {
      if (!_iteratorNormalCompletion && _iterator.return) {
        _iterator.return();
      }
    } finally {
      if (_didIteratorError) {
        throw _iteratorError;
      }
    }
  }

  return res;
}

function _generateRouters(type, routers) {
  var res = [];
  var _iteratorNormalCompletion2 = true;
  var _didIteratorError2 = false;
  var _iteratorError2 = undefined;

  try {
    for (var _iterator2 = routers[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
      var router = _step2.value;

      res.push(_generateRouter(type, router));
    }
  } catch (err) {
    _didIteratorError2 = true;
    _iteratorError2 = err;
  } finally {
    try {
      if (!_iteratorNormalCompletion2 && _iterator2.return) {
        _iterator2.return();
      }
    } finally {
      if (_didIteratorError2) {
        throw _iteratorError2;
      }
    }
  }

  return res;
}

},{"./2d/floor":5,"./2d/router":7,"./2d/wall":8,"./3d/floor":9,"./3d/router":11,"./3d/wall":12}],15:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Camera = exports.Camera = function (_THREE$OrthographicCa) {
  _inherits(Camera, _THREE$OrthographicCa);

  function Camera(width, height) {
    _classCallCheck(this, Camera);

    var _this = _possibleConstructorReturn(this, (Camera.__proto__ || Object.getPrototypeOf(Camera)).call(this, width / -2 / 30, width / 2 / 30, height / 2 / 30, height / -2 / 30, -500, 1000));

    _this.position.x = 16.5;
    _this.position.y = -6;
    _this.position.z = 10;

    _this.rotation.x = 0;
    _this.rotation.y = 0;
    _this.rotation.z = 0;
    return _this;
  }

  return Camera;
}(THREE.OrthographicCamera);

},{}],16:[function(require,module,exports){
"use strict";

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Camera = exports.Camera = function (_THREE$PerspectiveCam) {
  _inherits(Camera, _THREE$PerspectiveCam);

  function Camera(width, height) {
    _classCallCheck(this, Camera);

    var _this = _possibleConstructorReturn(this, (Camera.__proto__ || Object.getPrototypeOf(Camera)).call(this, 60, width / height, 1, 2000));

    _this.position.x = 20;
    _this.position.y = 10;
    _this.position.z = 20;

    _this.rotation.x = 0;
    _this.rotation.y = 0;
    _this.rotation.z = 0;
    return _this;
  }

  return Camera;
}(THREE.PerspectiveCamera);

},{}],17:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var Light = exports.Light = function () {
  function Light() {
    var color = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "#ffffff";
    var intensity = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0.4;

    _classCallCheck(this, Light);

    this.directional = _generateDirectional(color, intensity);
    this.ambient = _generateAmbient(color, intensity);
  }

  _createClass(Light, [{
    key: "getDirectional",
    value: function getDirectional() {
      return this.directional;
    }
  }, {
    key: "getAmbient",
    value: function getAmbient() {
      return this.ambient;
    }
  }]);

  return Light;
}();

function _generateDirectional(color, intensity) {
  var light = new THREE.DirectionalLight(color, intensity);
  light.position.set(0.0, 0.0, 10.0).normalize();
  return light;
}

function _generateAmbient(color, intensity) {
  return new THREE.AmbientLight(color, intensity);
}

},{}],18:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Scene = undefined;

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

var _camera = require("./2d/camera");

var _controls = require("./../utils/2d/controls");

var _camera2 = require("./3d/camera");

var _controls2 = require("./../utils/3d/controls");

var _light = require("./3d/light");

var _map = require("./../objects/map");

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var Scene = exports.Scene = function () {
  function Scene(type, map) {
    var elementId = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;
    var enableControls = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;

    _classCallCheck(this, Scene);

    this.elementId = elementId;
    this.map = _generateMap(type, map);
    this.renderer = _generateRenderer(elementId);
    this.camera = _generateCamera(type, elementId);
    this.light = _generateLight(type);
    if (enableControls) {
      this.controls = _generateControls(type, this.camera);
    } else {
      this.controls = null;
    }

    this.scene = _genreateScene(this.map, this.light);
  }

  _createClass(Scene, [{
    key: "setLocatorPosition",
    value: function setLocatorPosition() {
      var x = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 0;
      var y = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;
      var z = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 0;

      var locator = this.map.getLocator();
      locator.position.x = x;
      locator.position.y = -y;
      locator.position.z = z;
    }
  }, {
    key: "show",
    value: function show() {
      var animate = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : true;

      var closureCopy = this;

      if (this.elementId == null) {
        document.body.appendChild(this.renderer.domElement);
        window.addEventListener('resize', function () {
          closureCopy._onWindowResize();
        }, false);
      }

      if (this.controls != null) {
        this.controls.run(function () {
          closureCopy._render();
        });
      }

      if (animate) {
        this._animate();
      }
    }

  }, {
    key: "_onWindowResize",
    value: function _onWindowResize() {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();

      this.renderer.setSize(window.innerWidth, window.innerHeight);
      if (this.controls != null) {
        this.controls.handleResize();
      }

      this._render();
    }
  }, {
    key: "_animate",
    value: function _animate() {
      var closureCopy = this;
      requestAnimationFrame(function () {
        closureCopy._animate();
      });

      this.setLocatorPosition(window.currentPosition.x, window.currentPosition.y, window.currentPosition.z);

      if (this.controls != null) {
        this.controls.update();
      }

      this._render();
    }
  }, {
    key: "_render",
    value: function _render() {
      this.renderer.render(this.scene, this.camera);
    }
  }]);

  return Scene;
}();

function _generateRenderer(elementId) {
  var renderer;

  if (elementId == null) {
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
  } else {
    renderer = new THREE.WebGLRenderer({
      canvas: document.getElementById(elementId)
    });
  }

  renderer.setPixelRatio(window.devicePixelRatio);
  return renderer;
}

function _generateMap(type, map) {
  return new _map.Map(type, map);
}

function _generateCamera(type, elementId) {
  var width = window.innerWidth;
  var height = window.innerHeight;

  if (elementId != null) {
    width = document.getElementById("map-canvas").width;
    height = document.getElementById("map-canvas").height;
  }

  switch (type) {
    case '2d':
      return new _camera.Camera(width, height);
    case '3d':
      return new _camera2.Camera(width, height);
  }
}

function _generateLight(type) {
  switch (type) {
    case '2d':
      return null;
    case '3d':
      return new _light.Light();
  }
}

function _generateControls(type, camera) {
  switch (type) {
    case '2d':
      return new _controls.Controls(camera);
    case '3d':
      return new _controls2.Controls(camera);
  }
}

function _genreateScene(map, light) {
  var res = new THREE.Scene();

  if (light != null) {
    res.add(light.getDirectional());
    res.add(light.getAmbient());
  }

  res.add(map.getLocator());

  var levels = map.getLevels();
  for (var level in levels) {
    res.add(levels[level].getFloor());

    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
      for (var _iterator = levels[level].getWalls()[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
        var wall = _step.value;

        res.add(wall);
      }
    } catch (err) {
      _didIteratorError = true;
      _iteratorError = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion && _iterator.return) {
          _iterator.return();
        }
      } finally {
        if (_didIteratorError) {
          throw _iteratorError;
        }
      }
    }

    var _iteratorNormalCompletion2 = true;
    var _didIteratorError2 = false;
    var _iteratorError2 = undefined;

    try {
      for (var _iterator2 = levels[level].getRouters()[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
        var router = _step2.value;

        res.add(router);
      }
    } catch (err) {
      _didIteratorError2 = true;
      _iteratorError2 = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion2 && _iterator2.return) {
          _iterator2.return();
        }
      } finally {
        if (_didIteratorError2) {
          throw _iteratorError2;
        }
      }
    }
  }

  return res;
}

},{"./../objects/map":13,"./../utils/2d/controls":19,"./../utils/3d/controls":20,"./2d/camera":15,"./3d/camera":16,"./3d/light":17}],19:[function(require,module,exports){
'use strict';

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Controls = exports.Controls = function (_THREE$OrthographicTr) {
  _inherits(Controls, _THREE$OrthographicTr);

  function Controls(camera) {
    _classCallCheck(this, Controls);

    var _this = _possibleConstructorReturn(this, (Controls.__proto__ || Object.getPrototypeOf(Controls)).call(this, camera));

    _this.noZoom = false;
    _this.noPan = false;
    _this.noRotate = true;
    _this.noRoll = true;

    _this.target = new THREE.Vector3(16.5, -6, 0);
    return _this;
  }

  _createClass(Controls, [{
    key: 'run',
    value: function run(render) {
      this.addEventListener('change', render);
    }
  }]);

  return Controls;
}(THREE.OrthographicTrackballControls);

},{}],20:[function(require,module,exports){
'use strict';

var _typeof2 = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _typeof = typeof Symbol === "function" && _typeof2(Symbol.iterator) === "symbol" ? function (obj) {
  return typeof obj === "undefined" ? "undefined" : _typeof2(obj);
} : function (obj) {
  return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj === "undefined" ? "undefined" : _typeof2(obj);
};

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
    }
  }return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
  };
}();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }return call && ((typeof call === "undefined" ? "undefined" : _typeof(call)) === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function, not " + (typeof superClass === "undefined" ? "undefined" : _typeof(superClass)));
  }subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } });if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

var Controls = exports.Controls = function (_THREE$OrbitControls) {
  _inherits(Controls, _THREE$OrbitControls);

  function Controls(camera) {
    _classCallCheck(this, Controls);

    return _possibleConstructorReturn(this, (Controls.__proto__ || Object.getPrototypeOf(Controls)).call(this, camera));
  }

  _createClass(Controls, [{
    key: 'run',
    value: function run(render) {
      this.addEventListener('change', render);
    }
  }]);

  return Controls;
}(THREE.OrbitControls);

},{}]},{},[4]);
