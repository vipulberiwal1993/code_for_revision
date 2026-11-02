class Solution(object):
    
    '''
    For each slot, we need to find the left max and the right max, the min of both decides the height of the slot
    but we know only  min of leftMax and rightMax matters so, 2 pointer approach- skip the other one!
    '''
    def trap(self, array):
        leftMax = array[0]
        l = 0
        r = len(array)-1
        rightMax = array[-1]
        ans = 0

        while l <= r:
            if leftMax < rightMax: 
                ans += max(0, leftMax - array[l])
                leftMax = max(leftMax, array[l])
                l += 1
            else:
                ans += max(0, rightMax - array[r])
                rightMax = max(rightMax, array[r])
                r -= 1
        return ans


    '''
    For each slot, we need to find the left max and the right max, the min of both decides the height of the slot, 
    but optimized where we same the right max and left max in array and then calculate.
    '''
    def trapMemory(self, array):
        leftMaxList = [0]*len(array)
        rightMaxList = [0]*len(array)
        ans = 0

        leftMax = 0
        rightMax = 0
        for i in range(len(array)):
            leftMax = max(leftMax, array[i])
            leftMaxList[i] = leftMax
            rightMax = max(rightMax, array[len(array)-i-1])
            rightMaxList[len(array)-i-1] = rightMax
            
        for i in range(len(array)):
            ans += max(0, min(rightMaxList[i], leftMaxList[i]) - array[i])
        return ans


    '''
    For each slot, we need to find the left max and the right max, the min of both decides the height of the slot
    '''
    def trapBruteForce(self, array):
        ans = 0
        for i in range(len(array)):
            #left 
            l = i
            leftmax = array[i]
            while l >= 0:
                leftmax = max(leftmax, array[l])
                l -= 1

            #right
            r = i
            rightmax = array[i]
            while r < len(array):
                rightmax = max(rightmax, array[r])
                r += 1

            ans += max(0, min(leftmax, rightmax) - array[i])

        return ans
        
