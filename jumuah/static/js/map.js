function initMap() {
  var kaabaCoordinates = {lat: 21.4225, lng: 39.8262};
  var map = new google.maps.Map(document.getElementById('map'), {
    center: kaabaCoordinates,
    streetViewControl: false,
    zoom: 16
  });

  var marker = new google.maps.Marker({
    position: new google.maps.LatLng(kaabaCoordinates),
    map: map,
    draggable: true
});
  //listeners
  google.maps.event.addListener(map, 'click', function (event) {
      var latitude = event.latLng.lat();
      var longitude = event.latLng.lng();
      document.getElementById("latitude").value = latitude;
      document.getElementById("longitude").value = longitude;
      marker.setPosition(new google.maps.LatLng(latitude, longitude));
  });

  google.maps.event.addListener(marker, 'dragend', function (event) {
      document.getElementById("latitude").value = this.getPosition().lat();
      document.getElementById("longitude").value = this.getPosition().lng();
  });

}
