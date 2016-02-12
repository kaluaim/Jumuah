function initMap() {
  var kaabaCoordinates = {lat: 21.4225, lng: 39.8262};
  var map = new google.maps.Map(document.getElementById('map'), {
    center: kaabaCoordinates,
    streetViewControl: false,
    zoom: 16
  });

}
