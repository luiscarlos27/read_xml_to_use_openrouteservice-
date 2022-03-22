from xml.dom import minidom
import json
import requests

def print_xml(file):
    """
    :param file: path where it be the file
    :return: json with all information of the routes
    """
    doc = minidom.parse(file)
    items = doc.getElementsByTagName('ExtRoute')

    routes = []
    for i in range(len(items)):
        extRoute = items[i]
        route = items[i].attributes['RouteName'].value
        print("Start Route " + str(route))
        docTrip = items[i].getElementsByTagName('DocTrip')

        for j in range(len(docTrip)):
            ## set routes
            entity = {}
            ## number trip
            trip = docTrip[j].attributes['TripName'].value
            entity["route"] = route
            entity["trip"] = trip
            path = []
            indications = []

            docStop = docTrip[j].getElementsByTagName('DocStop')
            for k in range(len(docStop)):
                if k == 0:
                    #print("validations the header")
                    depot = docStop[k].attributes['LocationRefNumber'].value
                    longitudeDepot = docStop[k].attributes['Longitude'].value
                    latitudeDepot = docStop[k].attributes['Latitude'].value
                    path.append(
                        {"origin": "Depot", "name": depot, "longitude": longitudeDepot, "latitude": latitudeDepot})
                    #print(depot)
                elif k > 0:
                    docPath = docStop[k].getElementsByTagName('DocPath')
                    instructions = docStop[k].getElementsByTagName('DocDrivingDirections')
                    ### points
                    for n in range(len(docPath)):
                        point = docPath[n].getElementsByTagName('Point')

                        for m in range(len(point)):
                            latitude = point[m].attributes['Latitude'].value
                            longitude = point[m].attributes['Longitude'].value
                            orderPoint = point[m].attributes['PointNumber'].value
                            path.append({"origin": "path", "name": "", "order": orderPoint, "longitude": longitude,
                                         "latitude": latitude})

                    ### instructions
                    for o in range(len(instructions)):
                        line = instructions[o].getElementsByTagName('Line')

                        for p in range(len(line)):
                            text = line[p].attributes['Text'].value
                            latitudeI = line[p].attributes['Latitude'].value
                            longitudeI = line[p].attributes['Longitude'].value

                            indications.append({"text": text, "latitude": latitudeI, "longitude": longitudeI})

            entity["path"] = path
            entity["indications"] = indications
            routes.append(entity)
        #print("End Route " + str(route))
    return routes


def send_data_service(routes):
    """
    :param json:  json with all information of the routes
    :return: json with inditations the openrouteservice
    """
    data = []
    for i in range(1):
        value = {}
        value["route"] = routes[i]
        indicationsApi = []
        number_requests = convert_json_request(routes[i]["indications"])
        for request in number_requests:
            info = request_api(request)
            indicationsApi.append(json.loads(info))
        value["indicationsApi"] = indicationsApi
        data.append(value)
    return data

def request_api(data):
    """

    :param data:
    :return:
    """
    print(json.dumps(data))
    headers = {'Content-type': 'application/json'}
    resp = requests.post('http://localhost:8080/ors/v2/directions/driving-car/geojson', data=json.dumps(data),
                         headers=headers)
    return resp.text

def convert_json_request(json):
    """

    :param json:
    :return:
    """

    container = []
    coordinates = []
    max = 50
    j = 1
    for i in range(len(json)):
        if j < max:
            coordinates.append([float(json[i]["longitude"]), float(json[i]["latitude"])])
            j = j+1
        elif j == max:
            container.append(
                {"coordinates": coordinates, "elevation": "true", "instructions": "true", "instructions_format": "html",
                 "language": "es", "units": "m"})
            j = 1
            coordinates = []

        if i == (len(json)-1):
            container.append(
                {"coordinates": coordinates, "elevation": "true", "instructions": "true", "instructions_format": "html",
                 "language": "es", "units": "m"})

    return container

if __name__ == '__main__':
    data = print_xml("/home/students/Desktop/XMLCH")
    value = send_data_service(data)
    print(value)