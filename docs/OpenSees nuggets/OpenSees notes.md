
STKO seminar
====

# Displacement-based
* Requires a fine mesh for non-linear problems.
* Characteristic length = element.
* Shear not considered in sectionAggregator.
* If torsion included in both fibersection and aggregator, set –GJ of fibersection = 0.
* Element loads do not affect directly the section response.

# Force-based
* One element per member is enough.
* Characteristic length = gauss point.
* Shear considered in sectionAggregator.
* If torsion included in both fibersection and aggregator, set –GJ of fibersection = 0, or larger than torsional stiffness.
* Element loads affect directly the section response.

# Constraint Handler
Wrong HANDLERS can lead to singularities.

## Plain
* ```Condensate slave DOFs```.
* Pay attention to master-slave pairs.
* Only for homogeneous constraints.
* Only for identity constraint matrices.

## Transformation
* ```Condensate slave DOFs```.
* Pay attention to master-slave pairs.

## Lagrange
* ```Adds 1 row for each constraint equation```.
* The system is not positive-definite anymore.
* Pay attantion to master-slave pairs.
* Pay attention to duplicated constraints (over-constrained system).
* Do not use convergence tests on displacements.

# Penalty
* ```Does not change the system size```.
* Pay attention to the penalty parameters.
* Do not use convergence tests on unbalance.
