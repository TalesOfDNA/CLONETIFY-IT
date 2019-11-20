
def save(coordinates, file, file_no):
	fileName= file.split(".")[0]
	fileName = str(fileName) + "_Tracking_" + str(file_no) + ".txt"

	file = open(fileName, 'w')
	for item in coordinates:
		file.write("{0}\n".format(item))
	file.close()


    # n = len(cells)
    # total = n - 1
    # delete=[]

    # for j in range(0, total):
    #     for k in range(j+1, n):
    #         if abs(cells[j][0] - cells[k][0]) < 30:
    #             if abs(cells[j][1] - cells[k][1]) < 30:
    #                 if cells[j][2] > cells[k][2]:
    #                     delete.append(k)
    #                 else:
    #                     delete.append(j)
    #             else:
    #                 pass
    #         else:
    #             pass
                
    # print(delete)
    # for t in range(0,len(delete)):
    #     index = delete[t]
    #     cells.remove(cells[index])

    # for m in len(cells):
    #     cx = int(cells[m][0])
    #     cy = int(cells[m][1])
    #     cv2.circle(image_contours, (cx, cy), 5, (34,255,34), -1)
    #     x, y, w, h = cv2.boundingRect(i)
    #     # draw a green rectangle to visualize the bounding rect
    #     #cv2.rectangle(image_contours, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #     # get the min area rect
    #     rect = cv2.minAreaRect(i)
    #     box = cv2.boxPoints(rect)
    #     # convert all coordinates floating point values to int
    #     box = np.int0(box)
    #     # draw a red 'nghien' rectangle
    #     #cv2.drawContours(image_contours, [box], 0, (255, 0, 0), 2)
    #     hull = cv2.convexHull(i)
    #     #cv2.drawContours(image_contours,[hull],0,(0,0,0), 2)
    #     #cv2.fillPoly(image_edged3, [hull], (0,0,0))
    #     counter = counter + 1