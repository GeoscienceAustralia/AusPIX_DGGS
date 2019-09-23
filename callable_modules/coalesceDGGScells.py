# -*- coding: utf-8 -*-

'''
This code takes a bunch of DGGS cells and sees which can be coalesced into their parent cells.
This reduces the number of cell references but can complicate comparison based on DGGS a bit.

At this stage run the modules a few times until the same number of cells is returned.
Later will be improved using a recursive method.


Joseph Bell Geoscience Australia

'''


from AusPIXengine.dggs import RHEALPixDGGS


# make an instance
rdggs = RHEALPixDGGS()

# find cells that can be coalesced into a bigger cell
# makes things more complicated when using DGGS but saves on space and time somewhat ie less DGGS records
def coalesce(dggs):  # recieves a list of dggs cell names inside a poly

    newDGGSrow = list()  # declare

    #calculate number of baby cells that exist
    for aCell in dggs:
        # go through each cell and see how many have the same parent
        thisParent = aCell[:-1]  # parent for this cell
        # print('thisParent', thisParent)

        # count the number of cells with the same parent
        numChilds = 0  # initialise
        for cells in dggs:  # count the cells with the same parent
            if cells[:-1] == thisParent:
                numChilds += 1  #count

        if numChilds == 9 : # in the case of 9 children
            # when 9 children then only record parent
            if thisParent not in newDGGSrow:  # ie only recorded once
                newDGGSrow.append(thisParent)  # append parent to new list - do not record the children
        else:  # not 9 children
            if aCell not in newDGGSrow:
                newDGGSrow.append(aCell)  # add the child cell (item)




    # for item in newDGGSrow:
    #     print(item)
    return newDGGSrow
