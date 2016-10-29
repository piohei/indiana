export function getLocation(xElementId, yElementId, zElementId) {
  var x = _toNumber($("#${xElementId}").val());
  var y = _toNumber($("#${yElementId}").val());
  var z = _toNumber($("#${zElementId}").val());

  return {
    x: x,
    y: y,
    z: z
  }
}

export function getUpperCaseMAC(macElementId) {
  var rawMAC = $("#${macElementId}");

  if(!/^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/.test(rawMAC)) {
    throw "invalid MAC: ${rawMAC}";
  }

  return rawMAC.toUpperCase();
}

function _toNumber(x) {
  var n = Number(x);
  if (isNaN(n)) {
    throw "not a number " + x;
  }
  return n;
}
