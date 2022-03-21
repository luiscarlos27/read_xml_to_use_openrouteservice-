from xml.dom import minidom

def print_xml():
    doc = minidom.parse("/home/students/Desktop/XMLCH")
    items = doc.getElementsByTagName('ExtRoute')

    routes = []
    for i in range(len(items)):
        extRoute = items[i]
        route = items[i].attributes['RouteName'].value
        print("Start Route "+str(route))
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
                    print("validations the header")
                    depot = docStop[k].attributes['LocationRefNumber'].value
                    longitudeDepot = docStop[k].attributes['Longitude'].value
                    latitudeDepot = docStop[k].attributes['Latitude'].value
                    path.append({"origin": "Depot", "name": depot, "longitude": longitudeDepot, "latitude": latitudeDepot})
                    print(depot)
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
                            """path.append({"origin": "path", "name": "","order": orderPoint, "longitude": longitude,
                                        "latitude": latitude})
                            """

                    ### instructions
                    for o in range(len(instructions)):
                        line = instructions[o].getElementsByTagName('Line')

                        for p in range(len(line)):
                            text = line[p].attributes['Text'].value
                            latitudeI = line[p].attributes['Latitude'].value
                            longitudeI = line[p].attributes['Longitude'].value

                            indications.append({"text":text, "latitude": latitudeI, "longitude": longitudeI})

            entity["path"] = path
            entity["indications"] = indications
            routes.append(entity)
        print("End Route "+str(route))

    print(routes)

if __name__ == '__main__':
    print_xml()
