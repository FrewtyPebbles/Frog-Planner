plannerData = {}

--String separator
function splitString (inputstr, sep)
	if sep == nil then
			sep = "%s"
	end
	local t={}
	for str in string.gmatch(inputstr, "[^"..sep.."]+" ) do
		table.insert(t, str)
	end
	return t
end

--Remove encoding tag
function decodeUTF(string)
	return string:sub(3, #string - 1)
end

--Makes a matrix of the csv data
function dataMatrix (data)
	local columns = splitString(data,"\n")
	local matrix = {}
	for i = 1, table.getn(columns) do
		rows = splitString(columns[i],"`")
		table.insert(matrix,rows)
	end
	return matrix
end

--Print the csv file
function printCSV()
	for i = 1, table.getn(plannerData) do
		io.write("#########################################\n~~~~~~~~~~~~~~~"..plannerData[i][1].."~~~~~~~~~~~~~~~\nVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV\n\n")
		for j = 2, table.getn(plannerData[i]),2 do
			io.write(" -=- "..plannerData[i][j].." > "..plannerData[i][j+1].."\n\n")
		end
		io.write("_____________________________________________________\n")
	end
end

--TODAY PROCESS
function todayProcess(today)
	for i = 1, table.getn(plannerData) do
		if today == plannerData[i][1] then

			io.write("#########################################\n~~~~~~~~~~~~~~~"..plannerData[i][1].."~~~~~~~~~~~~~~~\nVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV\n\n")

			for j = 2, table.getn(plannerData[i]),2 do

				io.write(" -=- "..plannerData[i][j].." > "..plannerData[i][j+1].."\n\n")

			end
			
			io.write("_____________________________________________________\n")
			
		end
	end
end

--INITIALIZE DATA FOR SCHEDULES
function init(today)
	local foundDate = false
	for i = 1, table.getn(plannerData) do
		if today == plannerData[i][1] then
			foundDate = true
			io.write("(")

			for j = 2, table.getn(plannerData[i]),2 do

				io.write("(\""..plannerData[i][j].."\",\""..plannerData[i][j+1].."\")")
				if j < (table.getn(plannerData[i])-2) then
					io.write(",")
				end

			end
			
			io.write(")")
			
		end
	end
	if foundDate == false then
		io.write(today.."`time`task~missingtoday\r")
	end
end

--HANDLE DATA
function handleData(data, today, process)

	plannerData = dataMatrix(decodeUTF(data))

	if process == "show today" then

		todayProcess(today)

	elseif process == "show important" then

		printCSV()

	elseif process == "init" then

		init(today)

	end
end


--TASK PROCESS
function taskProcess(date, time, task)
	local foundDate = false
	for i = 1, table.getn(plannerData) do
		if date == plannerData[i][1] then
			--append table
			plannerData[i][table.getn(plannerData[i])]:sub(0, #plannerData[i][table.getn(plannerData[i])] - 1)
			table.insert( plannerData[i], time )
			table.insert( plannerData[i], task )
			foundDate = true
			break
		end
	end
	for i = 1, table.getn(plannerData) do
		io.write(plannerData[i][1])
		for j = 2, table.getn(plannerData[i]),1 do

			io.write("`"..plannerData[i][j])

		end
		io.write("\r")
	end
	if foundDate == false then
		io.write(date.."`time`task`"..time.."`"..task.."\r")
	end
end

--APPEND DATA
function appendData(data, date, time, task, process)

	plannerData = dataMatrix(decodeUTF(data))

	if process == "append task" then

		taskProcess(date,time,task)

	elseif process == "show important" then

		printCSV()

	end
end