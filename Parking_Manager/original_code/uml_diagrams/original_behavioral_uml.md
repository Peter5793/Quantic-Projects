@startuml EasyParkPlus Parking System
title EasyParkPlus Parking System Behavioral Sequence Diagram — ParkingManager

actor User
participant "ParkingView" as View
participant "ParkingController" as Controller
participant "ParkingFacility" as Facility
participant "ParkingSpace" as Space
participant "Vehicle" as Vehicle
participant "ChargingStation" as Charger
participant "BillingService" as Billing

group Create Facility
    User -> View: Create Facility (name, location, capacity)
    View -> Controller: create_facility(data)
    Controller -> Facility: create(data)
    Facility --> Controller: facilityCreated(id)
    Controller --> View: facilityCreated(id)
end

group Park Vehicle
    User -> View: Park Vehicle (plate, type)
    View -> Controller: request_park(vehicleInfo)
    Controller -> Facility: findAvailableSpace(vehicleInfo)
    alt space available
        Facility -> Space: reserve(spaceId, vehicleInfo)
        Space --> Facility: reserved(spaceId)
        Facility --> Controller: spaceReserved(spaceId)
        Controller -> Vehicle: start_parking_session(vehicleInfo, spaceId)
        Controller --> View: parked(spaceId)
    else no space
        Facility --> Controller: noSpace
        Controller --> View: parkingRejected(reason)
    end
end

group Start Charging
    User -> View: Start Charging (vehicleId, stationId)
    View -> Controller: start_charging(vehicleId, stationId)
    Controller -> Charger: request_start(sessionRequest)
    alt station accepts
        Charger --> Controller: sessionStarted(sessionId)
        Controller -> Billing: preauthorize_charge(sessionId, estimate)
        Billing --> Controller: preauth_ok
        Controller --> View: chargingStarted(sessionId)
    else station rejects
        Charger --> Controller: startRejected(reason)
        Controller --> View: chargingFailed(reason)
    end
end

group Stop Charging
    User -> View: Stop Charging (sessionId)
    View -> Controller: stop_charging(sessionId)
    Controller -> Charger: stop(sessionId)
    Charger --> Controller: stopped(details)
    Controller -> Billing: finalize_charge(details)
    Billing --> Controller: invoice(invoiceId)
    Controller --> View: chargingStopped(invoiceId)
end

group Remove Vehicle
    User -> View: Remove Vehicle (vehicleId)
    View -> Controller: end_parking(vehicleId)
    Controller -> Facility: releaseSpace(spaceId)
    Facility --> Controller: released(spaceId)
    Controller -> Billing: calculate_parking_fee(sessionId)
    Billing --> Controller: invoice(invoiceId)
    Controller --> View: vehicleRemoved(invoiceId)
end

group Query Lot Status
    User -> View: Get Lot Status
    View -> Controller: get_status()
    Controller -> Facility: fetch_status()
    Facility --> Controller: statusData
    Controller --> View: statusData
    View --> User: display(statusData)
end

note over Controller,Facility: Controller acts as a facade — keeps view thin and delegates business logic to domain
note over Charger,Billing: Charging service and Billing service are separate bounded contexts; communicate via events/APIs

@enduml
