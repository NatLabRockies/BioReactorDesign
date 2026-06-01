/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "codedFunctionObjectTemplate.H"
#include "volFields.H"
#include "read.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(gasHoldupFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    gasHoldupFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = be5063f0872ff9d3a8fa402c313317bc41bd69dd
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void gasHoldup_be5063f0872ff9d3a8fa402c313317bc41bd69dd(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const fvMesh& gasHoldupFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

gasHoldupFunctionObject::gasHoldupFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

gasHoldupFunctionObject::~gasHoldupFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool gasHoldupFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read gasHoldup sha1: be5063f0872ff9d3a8fa402c313317bc41bd69dd\n";
    }

//{{{ begin code
    #line 14 "/home/federico/OpenFOAM/federico-13/run/BioReactorDesign/tutorials_13/STR_rotatingMesh/system/functions/gasHoldup"

    fileName dir
    (
        mesh().time().globalPath()/
        "postProcessing"/
        name()/
        mesh().time().name()
    );

    mkDir(dir);
    file = new OFstream(dir/"gasHoldup.dat");

    file()<< "# Time" << tab << "gasHoldup" << tab << "gasHoldupMean" << endl;

//}}} end code

    return true;
}


Foam::wordList gasHoldupFunctionObject::fields() const
{
    if (false)
    {
        Info<<"fields gasHoldup sha1: be5063f0872ff9d3a8fa402c313317bc41bd69dd\n";
    }

    wordList fields;
//{{{ begin code
    #line 28 "/home/federico/OpenFOAM/federico-13/run/BioReactorDesign/tutorials_13/STR_rotatingMesh/system/functions/gasHoldup"

    fields.append("alpha.gas");
    fields.append("alphaMean.gas");

//}}} end code

    return fields;
}


bool gasHoldupFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute gasHoldup sha1: be5063f0872ff9d3a8fa402c313317bc41bd69dd\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool gasHoldupFunctionObject::write()
{
    if (false)
    {
        Info<<"write gasHoldup sha1: be5063f0872ff9d3a8fa402c313317bc41bd69dd\n";
    }

//{{{ begin code
    #line 32 "/home/federico/OpenFOAM/federico-13/run/BioReactorDesign/tutorials_13/STR_rotatingMesh/system/functions/gasHoldup"

    scalar alphaTreshold = Foam::read<doubleScalar>("5.00000000e-01");

    const volScalarField& alpha =
        mesh().lookupObject<volScalarField>("alpha.gas");

    const scalarField& V = mesh().V();

    const scalar gasHoldup
    (
        gSum(neg(alpha - alphaTreshold)*alpha*V)
       /gSum(neg(alpha - alphaTreshold)*V)
    );

    file() << mesh().time().userTimeValue() << tab << gasHoldup << endl;

//}}} end code

    return true;
}


bool gasHoldupFunctionObject::end()
{
    if (false)
    {
        Info<<"end gasHoldup sha1: be5063f0872ff9d3a8fa402c313317bc41bd69dd\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

