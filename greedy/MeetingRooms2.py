
import heapq
from bisect import bisect_left, bisect_right


class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        # Use binary search to calculate the maximum number
        # of overlapping meetings.
        return self.binarySearch(intervals)

    def countingMethod(self, intervals: list[list[int]]) -> int:
        # Sort meetings by start time.
        startOrder = sorted(intervals)

        # Sort meetings independently by end time.
        endOrder = sorted(intervals, key=lambda x: x[1])

        # i tracks the next meeting starting.
        # j tracks the earliest meeting ending.
        i = 0
        j = 0

        # Number of rooms currently occupied.
        count = 0

        # Maximum rooms occupied simultaneously.
        maxRooms = 0

        while i < len(intervals):
            # If the earliest meeting ends at or before
            # the next meeting starts, its room can be reused.
            #
            # Meeting intervals are treated as [start, end),
            # so meetings ending and starting at the same
            # time do not overlap.
            if endOrder[j][1] <= startOrder[i][0]:
                count -= 1
                j += 1

            # Allocate a room for the meeting starting now.
            count += 1

            # Track the maximum number of occupied rooms.
            maxRooms = max(maxRooms, count)

            # Process the next meeting.
            i += 1

        return maxRooms

        # Time: O(N log N) - sorting dominates.
        # Space: O(N) - two sorted arrays.

    def heapMethod(self, intervals):
        # Handle empty input.
        if not intervals:
            return 0

        # Process meetings in ascending start-time order.
        startTimes = sorted(intervals)

        # Min-heap stores end times of meetings
        # currently occupying conference rooms.
        heap = []

        for start, end in startTimes:
            # If the earliest ending meeting has finished,
            # its room can be reused.
            if heap and heap[0] <= start:
                heapq.heappop(heap)

            # Allocate a room for the current meeting,
            # or reuse the room freed above.
            heapq.heappush(heap, end)

        # Each remaining heap entry represents a room
        # allocated by the algorithm.
        return len(heap)

        # Time: O(N log N) - sorting and heap operations.
        # Space: O(N) - sorted meetings and heap.

    def binarySearch(self, intervals):
        # Sort all meeting start times independently.
        startTimes = sorted(x[0] for x in intervals)

        # Sort all meeting end times independently.
        endTimes = sorted(x[1] for x in intervals)

        # Maximum number of simultaneous meetings.
        ans = 0

        # Overlap can only increase when a meeting starts.
        # Therefore, checking each start time is sufficient.
        for start in startTimes:

            # Count meetings that started at or before
            # the current time.
            #
            # bisect_right returns the insertion position
            # after all values equal to start.
            startedMeetings = bisect_right(startTimes, start)

            # Count meetings that ended at or before
            # the current time.
            #
            # Rooms become available immediately when
            # meetings end, including at this exact time.
            endedMeetings = bisect_right(endTimes, start)

            # Active meetings = started - ended.
            # Every active meeting needs a separate room.
            ans = max(ans, startedMeetings - endedMeetings)

        return ans

        # Time: O(N log N)
        # Sorting: O(N log N)
        # N iterations with binary search: O(N log N)
        #
        # Space: O(N) - two sorted arrays.
