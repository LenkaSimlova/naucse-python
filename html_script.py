zacatek = """<!doctype html>
<html>
<head>
	<script src="https://api.mapy.cz/loader.js"></script>
	<script>Loader.load()</script>
</head>

<body>
	<div id="mapa" style="width:600px; height:400px;"></div>
    <script type="text/javascript">
        var fotky = """
        
konec = """var center = SMap.Coords.fromWGS84(0.0, 0.0);
        var m = new SMap(JAK.gel("mapa"), center, 1);
        m.addDefaultLayer(SMap.DEF_BASE).enable();
        m.addDefaultControls();

        var layer = new SMap.Layer.Marker();
        m.addLayer(layer);
        layer.enable();

var clusterer = new SMap.Marker.Clusterer(m);
layer.setClusterer(clusterer);
var markers = [];

//for (var fotka in fotky) {
for (i = 0; i < fotky.length; i++) {
var fotka = fotky[i];
    var card = new SMap.Card();
    card.getHeader().innerHTML = "<strong>"+fotka['new_name']+"</strong>";
    card.getBody().innerHTML = "<img src="+fotka['new_path']+" width=250>";

    var souradnice = SMap.Coords.fromWGS84(fotka['longitude'], fotka['latitude']);
    var marker = new SMap.Marker(souradnice);
    marker.decorate(SMap.Marker.Feature.Card, card);
    markers.push(marker);
}
        layer.addMarker(markers);
</script>
</body>
</html>"""

